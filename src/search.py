# ================================================================== #
# Desafio MBA Engenharia de Software com IA - Full Cycle             #
# ================================================================== #
# Autor: Jesse de Oliveira                                           #
# Email: jesse.oli@hotmail.com                                       #
# Data: 03/09/2025                                                   #
# Versão: 1.0.0                                                      #
# ================================================================== # 
 
import os
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from dotenv import load_dotenv
load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
Nome da empresa | Faturamento | Ano de fundação
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS E RESPOSTAS CORRETAS:
PERGUNTA: "Qual o faturamento da Empresa SuperTechIABrazil?"
RESPOSTA: "O faturamento foi de 10 milhões de reais."

PERGUNTA: "Qual o ano de fundação da empresa Aurora Eventos ME?"
RESPOSTA: "O ano foi 1995."

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
)

def search_prompt(pergunta = ""):
    if not pergunta:
        return "Nenhuma pergunta foi feita."
    contexto = ""
    store_result = store.similarity_search_with_score(pergunta, k=3)
    for (doc, i) in store_result:
        contexto += doc.page_content
    chat_prompt = ChatPromptTemplate.from_messages([PROMPT_TEMPLATE])
    messages = chat_prompt.format_messages(contexto=contexto, pergunta=pergunta)
    model = ChatGoogleGenerativeAI(
        model=os.getenv("LLM_MODEL"),
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    result = model.invoke(messages)
    return result.content