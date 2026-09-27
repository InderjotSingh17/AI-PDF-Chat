# AI PDF Chat

A backend-powered **AI PDF Chat application** that allows users to upload PDF documents and ask questions about their content using **Retrieval-Augmented Generation (RAG)**.

The system extracts text from PDFs, splits it into chunks, generates semantic embeddings, stores them in PostgreSQL using **pgvector**, retrieves the most relevant chunks for a user's question, and uses **Google Gemini** to generate a context-aware answer.

---

## 🚀 Features

* 📄 Upload PDF documents
* 🔍 Extract text from PDFs
* ✂️ Split documents into smaller chunks
* 🧠 Generate semantic embeddings using Sentence Transformers
* 🗄️ Store embeddings in PostgreSQL with pgvector
* 🔎 Perform vector similarity search
* 📚 Retrieval-Augmented Generation (RAG)
* 🤖 Generate answers using Google Gemini
* 💬 Maintain conversation history
* ⚡ FastAPI REST API
* 🧩 SQLAlchemy ORM

---

## 🏗️ Architecture

```text
                    AI PDF CHAT
                         │
                         ▼
                  ┌─────────────┐
                  │   FastAPI   │
                  └──────┬──────┘
                         │
                  Upload PDF
                         │
                         ▼
                  ┌─────────────┐
                  │ PDF Extract │
                  └──────┬──────┘
                         │
                         ▼
                    Chunk Text
                         │
                         ▼
                Sentence Transformer
                         │
                         ▼
                   Embeddings
                         │
                         ▼
              PostgreSQL + pgvector
                         │
                         │
              ┌──────────┴──────────┐
              │                     │
         User Question              │
              │                     │
              ▼                     │
        Question Embedding          │
              │                     │
              ▼                     │
       Vector Similarity Search ◄───┘
              │
              ▼
        Relevant PDF Chunks
              │
              ▼
           RAG Context
              │
              ▼
       Google Gemini
              │
              ▼
         AI Response
```

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

### AI / GenAI

* Sentence Transformers
* `all-MiniLM-L6-v2`
* Google Gemini
* Retrieval-Augmented Generation (RAG)

### Vector Database

* PostgreSQL
* pgvector

### PDF Processing

* PyPDF

---

## 📂 Project Structure

```text
AI-PDF-Chat/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── dependencies.py
│   │
│   ├── routers/
│   │   └── chat.py
│   │
│   └── services/
│       ├── pdf.py
│       ├── chunking.py
│       ├── embeddings.py
│       ├── rag.py
│       └── llm.py
│
├── uploads/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> `uploads/` and `.env` are excluded from version control using `.gitignore`.

---

## ⚙️ How It Works

### 1. Upload a PDF

The user uploads a PDF through the FastAPI `/upload` endpoint.

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
```

### 2. Generate Embeddings

Each text chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The model generates a **384-dimensional embedding** for each chunk.

```text
Text Chunk
    ↓
Sentence Transformer
    ↓
384-dimensional Vector
```

### 3. Store in PostgreSQL

The chunks and their embeddings are stored in PostgreSQL.

```text
document_chunks
├── document_id
├── chunk_text
└── embedding
```

The `embedding` column uses the PostgreSQL **pgvector** extension.

### 4. Ask a Question

The user sends a question to:

```text
POST /chat
```

The question is converted into an embedding using the same embedding model.

### 5. Vector Similarity Search

The question embedding is compared against the stored PDF embeddings.

The system retrieves the most relevant chunks using **cosine similarity/distance**.

```text
User Question
      ↓
Question Embedding
      ↓
pgvector Similarity Search
      ↓
Top Relevant Chunks
```

### 6. RAG

The retrieved PDF chunks are added to the prompt as context.

```text
Question
   +
Retrieved PDF Context
   +
Conversation History
   ↓
Gemini
```

### 7. Generate Answer

Gemini generates an answer based on the retrieved information rather than relying only on its general knowledge.

---

## 🔌 API Endpoints

### Health Check

```http
GET /
```

Returns:

```json
{
  "message": "AI PDF Chat API is running"
}
```

---

### Upload PDF

```http
POST /upload
```

Accepts a PDF file and:

* Saves the PDF
* Extracts its text
* Creates chunks
* Generates embeddings
* Stores chunks and embeddings in PostgreSQL

Example response:

```json
{
  "message": "PDF uploaded and embeddings stored successfully",
  "filename": "example.pdf",
  "number_of_chunks": 10,
  "id": 1
}
```

---

### Chat With PDF

```http
POST /chat
```

Request:

```json
{
  "document_id": 1,
  "question": "What is this document about?"
}
```

Example response:

```json
{
  "answer": "The document discusses...",
  "document_id": 1,
  "retrieved_chunks": 5
}
```

---

## 🔧 Setup

### 1. Clone the repository

```bash
git clone https://github.com/InderjotSingh17/AI-PDF-Chat.git
```

```bash
cd AI-PDF-Chat
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/ai_pdf_chat

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 6. Start PostgreSQL

Make sure PostgreSQL is running and the database exists.

The PostgreSQL `vector` extension must also be enabled:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 7. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🧪 Example Workflow

### Upload

```text
POST /upload
       ↓
example.pdf
       ↓
Extract text
       ↓
Create chunks
       ↓
Generate embeddings
       ↓
Store in PostgreSQL
```

### Ask

```text
POST /chat

{
  "document_id": 1,
  "question": "What is this document about?"
}
```

### Retrieval

```text
Question
   ↓
Embedding
   ↓
pgvector
   ↓
Relevant chunks
```

### Generation

```text
Relevant chunks
      +
Question
      +
Conversation history
      ↓
Gemini
      ↓
Answer
```

---

## 🔐 Environment Variables

The application uses environment variables for sensitive configuration.

```env
DATABASE_URL=
GEMINI_API_KEY=
```

Never commit `.env` to GitHub.

---

## 🎯 Learning Goals

This project was built to gain practical experience with:

* Building AI-powered backend systems
* FastAPI
* PostgreSQL
* SQLAlchemy
* Vector databases
* Embeddings
* Semantic search
* Retrieval-Augmented Generation
* LLM integration
* Conversational memory
* Designing modular AI services

---

## 🔮 Future Improvements

Potential improvements include:

* Streaming LLM responses
* Authentication and user-specific documents
* Better document chunking strategies
* Metadata-based retrieval
* Multiple document conversations
* Hybrid search
* Reranking
* Background document processing
* Rate limiting
* Docker deployment
* Cloud deployment
* Evaluation of RAG retrieval quality

---

## 👨‍💻 Author

**Inderjot Singh**

B.Tech CSE (AI/ML)

GitHub: [InderjotSingh17](https://github.com/InderjotSingh17)

---

## ⭐ Project Summary

**AI PDF Chat** demonstrates an end-to-end Retrieval-Augmented Generation pipeline:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
PostgreSQL + pgvector
 ↓
Semantic Retrieval
 ↓
RAG
 ↓
Gemini
 ↓
AI Answer
```

Built to understand and implement the core architecture behind modern **RAG-based GenAI applications**.
