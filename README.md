# Retrieval-Augmented Generation (RAG)

A modular Retrieval-Augmented Generation system that loads documents from multiple file formats, converts them into semantic embeddings, stores them in a FAISS vector database, retrieves the most relevant content for a user query, and uses an LLM to generate a context-aware summary.

## Overview

Traditional language models can struggle when answering questions about information that is stored in external documents.

This project implements a complete RAG pipeline that combines:

* Document ingestion
* Text chunking
* Semantic embeddings
* Vector similarity search
* Context retrieval
* LLM-based response generation

The system allows information stored in local documents to be searched semantically and used as context for generating relevant answers.

## Key Features

* Supports multiple document formats
* Automatic document ingestion
* Recursive text chunking
* Semantic embeddings using Sentence Transformers
* FAISS-based vector similarity search
* Persistent vector index and metadata
* Configurable top-k retrieval
* LLM-powered contextual summarization
* Modular Python architecture
* Environment variable support using `.env`

## Supported Documents

The data loader currently supports:

* PDF
* TXT
* CSV
* Excel
* Word
* JSON

Documents placed inside the `data` directory are automatically discovered and loaded into the LangChain document format.

## RAG Pipeline

```text
                 Documents
                     │
                     ▼
             Document Ingestion
                     │
                     ▼
              Text Extraction
                     │
                     ▼
              Text Chunking
                     │
                     ▼
          Sentence Transformer
          all-MiniLM-L6-v2
                     │
                     ▼
             Vector Embeddings
                     │
                     ▼
              FAISS Index
                     │
                     │
User Query ──────────┘
      │
      ▼
Query Embedding
      │
      ▼
Similarity Search
      │
      ▼
Top-K Relevant Chunks
      │
      ▼
Context Construction
      │
      ▼
Groq LLM
gemma2-9b-it
      │
      ▼
Context-Aware Summary
```

## How It Works

### 1. Document Ingestion

The system scans the `data` directory and identifies supported files.

It uses LangChain document loaders to extract content from PDF, TXT, CSV, Excel, Word, and JSON files.

### 2. Text Chunking

Large documents are divided into smaller chunks using `RecursiveCharacterTextSplitter`.

Default configuration:

* Chunk size: `1000`
* Chunk overlap: `200`

The overlap helps preserve context between adjacent chunks.

### 3. Embedding Generation

Each text chunk is converted into a numerical vector using the Sentence Transformers model:

```text
all-MiniLM-L6-v2
```

These embeddings represent the semantic meaning of the document content.

### 4. Vector Storage

The generated embeddings are stored using FAISS.

The project uses:

```text
FAISS IndexFlatL2
```

The FAISS index and document metadata are persisted locally inside the `faiss_store` directory.

### 5. Semantic Retrieval

When a user submits a query, the query is converted into an embedding using the same embedding model.

FAISS then performs similarity search and retrieves the most relevant document chunks.

The number of retrieved results can be controlled using `top_k`.

### 6. LLM Generation

The retrieved document chunks are combined into a context.

The context and user query are passed to a Groq-hosted LLM using:

```text
gemma2-9b-it
```

The model then generates a summary based on the retrieved context.

## Tech Stack

### Programming Language

* Python

### LLM & AI

* Groq
* Gemma 2 9B IT
* Sentence Transformers

### RAG Framework

* LangChain
* LangChain Community

### Vector Database

* FAISS

### Document Processing

* PyPDF
* LangChain document loaders
* DOCX loader
* Excel loader
* CSV loader
* JSON loader

### Utilities

* python-dotenv
* NumPy
* Pickle

## Project Structure

```text
RAG/
│
├── data/
│   ├── pdf/
│   ├── text_files/
│   └── vector_store/
│
├── faiss_store/
│   ├── faiss.index
│   └── metadata.pkl
│
├── notebook/
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── embedding.py
│   ├── search.py
│   └── vectorstore.py
│
├── tools/
│   └── check_imports.py
│
├── app.py
├── requirements.txt
└── .env
```

## Core Components

### `data_loader.py`

Responsible for discovering and loading supported documents from the `data` directory.

It converts different file formats into a common LangChain document structure.

### `embedding.py`

Responsible for:

* Splitting documents into chunks
* Loading the Sentence Transformer model
* Generating embeddings

### `vectorstore.py`

Responsible for:

* Creating the FAISS index
* Adding document embeddings
* Saving the index
* Loading the persisted index
* Performing similarity searches

### `search.py`

Connects retrieval with the LLM.

It:

1. Loads or builds the FAISS vector store.
2. Converts the user query into an embedding.
3. Retrieves relevant document chunks.
4. Builds the context.
5. Sends the context to the Groq LLM.
6. Returns the generated summary.

### `app.py`

Acts as the main entry point for testing the RAG pipeline.

## Installation

Clone the repository:

```bash
git clone https://github.com/amaanbkn/RAG.git
cd RAG
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Make sure the API key is kept private and is not committed to GitHub.

## Add Your Documents

Place your documents inside the `data` directory.

Example:

```text
data/
├── pdf/
│   └── document.pdf
├── text_files/
│   └── notes.txt
└── ...
```

The document loader automatically searches the data directory for supported file types.

## Run the Project

Run the main application:

```bash
python app.py
```

The current implementation builds or loads the FAISS vector store and performs a sample retrieval query.

## Example Query

The project includes example queries such as:

```text
What is error detection?
```

and:

```text
What is attention mechanism?
```

The system retrieves the most relevant document chunks and generates a summary using the LLM.

## Retrieval Example

```python
rag_search = RAGSearch()

summary = rag_search.search_and_summarize(
    "What is attention mechanism?",
    top_k=3
)

print(summary)
```

## Vector Search Configuration

The default embedding configuration is:

```text
Embedding Model: all-MiniLM-L6-v2
Chunk Size: 1000
Chunk Overlap: 200
Vector Index: FAISS IndexFlatL2
Default Top-K: 5
```

## Why RAG?

Retrieval-Augmented Generation allows an LLM to use external information during response generation.

Instead of relying only on information learned during model training, the system retrieves relevant content from the provided documents and uses that content as context.

This makes the architecture useful for:

* Document question answering
* Knowledge-base assistants
* Technical documentation search
* Research document analysis
* Internal knowledge systems
* Personal document assistants

## Advantages

* Works with user-provided documents
* Supports semantic rather than simple keyword search
* Uses persistent local FAISS storage
* Modular architecture
* Supports multiple document formats
* Separates retrieval from generation
* Can be extended with different embedding models or LLMs

## Future Improvements

* Add a proper interactive chat interface
* Add conversation memory
* Add source citations to generated responses
* Add configurable similarity thresholds
* Add metadata filtering
* Support additional vector databases
* Add document upload functionality
* Add streaming responses
* Add RAG evaluation metrics
* Add hybrid keyword and semantic retrieval
* Deploy the application as a web service

## License

This project is intended for learning and experimentation with Retrieval-Augmented Generation, semantic search, vector databases, and LLM-based applications.
