# ================================================================== #
# Desafio MBA Engenharia de Software com IA - Full Cycle             #
# ================================================================== #
# Autor: Jesse de Oliveira                                           #
# Email: jesse.oli@hotmail.com                                       #
# Data: 03/09/2025                                                   #
# Versão: 1.0.0                                                      #
# ================================================================== #  

import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from dotenv import load_dotenv
load_dotenv()
PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    pdf_file = Path(PDF_PATH) / "document.pdf"
    documents = PyPDFLoader(str(pdf_file)).load()
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, 
        add_start_index=False
    ).split_documents(documents)

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in("", "none")}
        )
        for d in splits
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

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

    store.add_documents(documents=enriched, ids=ids)

    print(f"✅ Documentos processados e armazenados com sucesso!")
    print(f"Total de chunks: {len(splits)}")
    print(f"Total de enriched: {len(enriched)}")
    print(f"Coleção: {os.getenv('PG_VECTOR_COLLECTION_NAME')}")

if __name__ == "__main__":
    ingest_pdf()