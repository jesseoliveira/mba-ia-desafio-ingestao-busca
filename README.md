# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de busca semântica RAG (Retrieval-Augmented Generation) que permite ingerir documentos PDF em um banco vetorial e realizar consultas através de um chat interativo.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

- **Python 3.8+** ([Download Python](https://www.python.org/downloads/))
- **Docker & Docker Compose** ([Download Docker](https://www.docker.com/get-started))
- **Git** ([Download Git](https://git-scm.com/downloads))
- **Chave API do Google Generative AI** ([Google AI Studio](https://makersuite.google.com/app/apikey))

## 🚀 Configuração e Instalação

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/mba-ia-desafio-ingestao-busca.git
cd mba-ia-desafio-ingestao-busca
```

### 2️⃣ Configure o ambiente virtual Python

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure as variáveis de ambiente

1. **Copie o arquivo de exemplo:**
   ```bash
   # Windows:
   copy env.example .env
   # Linux/Mac:
   cp env.example .env
   ```

2. **Edite o arquivo `.env`** com suas configurações:
   ```env
   # API Google Generative AI
   GOOGLE_API_KEY=sua_chave_api_google_aqui
   EMBEDDING_MODEL=models/embedding-001
   LLM_MODEL=gemini-pro

   # Configurações do Banco de Dados PostgreSQL + pgvector
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
   PG_VECTOR_COLLECTION_NAME=documents

   # Configurações de Arquivos
   PDF_PATH=.
   ```

   > ⚠️ **Importante:** Substitua `sua_chave_api_google_aqui` pela sua chave real da API do Google Generative AI.

### 5️⃣ Inicie o banco de dados PostgreSQL com pgvector

```bash
# Iniciar os containers Docker
docker-compose up -d

# Verificar se os containers estão rodando
docker-compose ps
```
   > 💡 **Dica:** Use a extenção "Database Management for MySQL/MariaDB, PostgreSQL" no VSCode ou Cursor para acessar o banco do PGVector

Aguarde alguns segundos para que o banco inicialize completamente e a extensão `vector` seja criada.

### 6️⃣ Prepare seu documento PDF

Certifique-se de que existe um arquivo chamado `document.pdf` na raiz do projeto. Este é o documento que será processado e indexado para busca.

## 🔄 Execução do Sistema

### 📥 Passo 1: Ingerir o documento PDF

Execute o script de ingestão para processar e armazenar o documento no banco vetorial:

```bash
python src/ingest.py
```

**Saída esperada:**
```
✅ Documentos processados e armazenados com sucesso!
Total de chunks: X
Total de enriched: X
Coleção: documents
```

### 💬 Passo 2: Iniciar o chat interativo

Após a ingestão bem-sucedida, inicie o chat:

```bash
python src/chat.py
```

**Saída esperada:**
```
================================================================================
                      Bem-vindo ao nosso chat via terminal!
                      Quando quiser encerrar, digite 'sair'
================================================================================

1) Qual sua dúvida? (digite 'sair' para encerrar): 
```

## 💡 Como usar

1. **Faça perguntas** sobre o conteúdo do documento PDF
2. **Digite 'sair'** para encerrar o chat
3. As respostas são baseadas **exclusivamente** no conteúdo do documento

### Exemplos de perguntas:
- "Qual é o faturamento da empresa X?"
- "Em que ano a empresa Y foi fundada?"
- "Quais são as principais empresas mencionadas?"

## 🔧 Scripts Disponíveis

| Script | Descrição | Como executar |
|--------|-----------|---------------|
| `src/ingest.py` | Processa e armazena o documento PDF no banco vetorial | `python src/ingest.py` |
| `src/chat.py` | Interface de chat para consultas | `python src/chat.py` |
| `src/search.py` | Módulo de busca (usado pelos outros scripts) | Importado automaticamente |

## 🛠️ Solução de Problemas

### Problema: Erro de conexão com o banco

**Solução:**
```bash
# Reiniciar os containers
docker-compose down
docker-compose up -d

# Aguardar inicialização completa
docker-compose logs postgres
```

### Problema: Erro na API do Google

**Verificações:**
1. Confirme se a chave API está correta no arquivo `.env`
2. Verifique se a API está habilitada no [Google Cloud Console](https://console.cloud.google.com/)
3. Confirme se há créditos disponíveis na conta

### Problema: Documento não encontrado

**Verificações:**
1. Confirme se existe um arquivo `document.pdf` na raiz do projeto
2. Verifique as permissões de leitura do arquivo
3. Confirme se a variável `PDF_PATH` está correta no `.env`

### Problema: Erro de dependências

**Solução:**
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Se houver conflitos, criar novo ambiente virtual
deactivate
rm -rf venv
python -m venv venv
# Ativar o ambiente e reinstalar
```

## 📁 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── src/
│   ├── chat.py          # Interface de chat interativo
│   ├── ingest.py        # Processamento e ingestão de PDF
│   └── search.py        # Motor de busca semântica
├── document.pdf         # Documento para processar
├── docker-compose.yml   # Configuração do PostgreSQL
├── env.example          # Exemplo de variáveis de ambiente
├── requirements.txt     # Dependências Python
└── README.md           # Este arquivo
```

## 🔄 Reiniciar o Sistema

Para reiniciar completamente o sistema:

```bash
# Parar containers
docker-compose down

# Remover volumes (limpa dados)
docker-compose down -v

# Reiniciar
docker-compose up -d

# Re-executar ingestão
python src/ingest.py
```

## 📞 Suporte

- **Autor:** Jesse de Oliveira
- **Email:** jesse.oli@hotmail.com
- **Versão:** 1.0.0

---

> 💡 **Dica:** Mantenha o ambiente virtual sempre ativado quando executar os scripts e certifique-se de que o Docker está rodando antes de iniciar qualquer processo.