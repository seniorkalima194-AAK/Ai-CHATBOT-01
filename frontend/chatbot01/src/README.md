<<<<<<< HEAD
# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])

```

You can also install [eslint-plugin-react-x](https://npmx.dev/package/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://npmx.dev/package/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])

```
=======
# Ai-CHATBOT
The Ai chatbot that will be able to answer students questions according to the specific syllable ( TIE ) of Tanzania offline later on i would like to make the Ai be adaptive but for now focused on the building the Ai chatbot first we work in team of four people including me as there leaders



<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=1E3A8A&height=220&section=header&text=Offline%20AI%20Chatbot&fontSize=50&fontColor=FFFFFF&fontAlignY=38&desc=Local%20RAG%20Educational%20Assistant&descAlignY=58&descSize=18" width="100%"/>
</div>

<p align="center">

![Status](https://img.shields.io/badge/Status-Under%20Development-0A66C2?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-0.1-blueviolet?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Gemma](https://img.shields.io/badge/Gemma-LLM-4285F4?style=for-the-badge&logo=google&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Enabled-purple?style=for-the-badge)

</p>

# 🎓 Offline AI Chatbot

> An offline-first educational AI chatbot that answers student questions using locally stored learning materials through Retrieval-Augmented Generation (RAG) and a locally hosted **Gemma** Large Language Model (LLM).

The system is designed to run on a local computer or school server and remain functional without external Internet access during normal operation.

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Project Goals](#-project-goals)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How the AI Works](#-how-the-ai-works)
- [Knowledge Ingestion Pipeline](#-knowledge-ingestion-pipeline)
- [Quick Start](#-quick-start)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [Testing and Evaluation](#-testing-and-evaluation)
- [Development Roadmap](#-development-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📌 About the Project

**Offline AI Chatbot** is the standalone AI component planned for a larger Offline Adaptive Learning System.

The chatbot combines:

- A locally hosted **Gemma** LLM for language generation
- **Retrieval-Augmented Generation (RAG)** for curriculum-grounded answers
- An embedding model for semantic search
- A local vector database for educational knowledge
- A **FastAPI** backend for application logic and API access
- A **React** frontend for the student chat interface

Instead of depending on a cloud AI service for every question, the chatbot retrieves relevant information from a locally prepared knowledge base and gives that information to Gemma as context.

### Core principle

```text
Student Question
      ↓
Semantic Retrieval
      ↓
Relevant Learning Content
      ↓
Gemma
      ↓
Grounded Answer
```

The goal is not simply to create a generic chatbot. The goal is to create an AI tutor that is **grounded in the learning materials available to the school**.

---

## 🎯 Project Goals

The first version focuses on building a reliable standalone AI chatbot capable of:

- Receiving student questions
- Searching local educational materials
- Retrieving relevant content
- Generating answers with Gemma
- Returning supporting source content
- Operating without external Internet access at runtime
- Maintaining basic conversational context
- Providing a clean API that can later be integrated into the full learning system

---

## ✨ Key Features

- 🔌 **Offline-first** — the LLM, vector store, and knowledge base run locally
- 📚 **Knowledge-grounded** — answers are based on retrieved educational content
- 🧠 **RAG pipeline** — semantic retrieval is performed before response generation
- 🤖 **Local Gemma LLM** — no external LLM API is required during normal runtime
- 🔎 **Semantic search** — questions are matched by meaning rather than keywords alone
- 📄 **Document ingestion** — learning materials can be processed into searchable chunks
- 📖 **Source-aware answers** — retrieved chunks can be returned with the generated response
- 📡 **REST API** — the chatbot is exposed through FastAPI
- 💻 **Web interface** — students interact with the AI through a React chat application
- 🧪 **Evaluation-ready** — the architecture supports retrieval and answer-quality testing

---

## 🏗️ System Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│                        STUDENT DEVICE                         │
│                                                               │
│                    React Web Application                      │
│                                                               │
│   ┌───────────────────────────────────────────────────────┐   │
│   │                    Chat Interface                     │   │
│   │                                                       │   │
│   │ Student Question ────────────────► Send              │   │
│   │                                                       │   │
│   │ ◄─────────────────────────────── AI Response          │   │
│   └───────────────────────────────┬───────────────────────┘   │
└────────────────────────────────────┼──────────────────────────┘
                                     │
                                HTTP / REST
                                     │
                                     ▼
┌───────────────────────────────────────────────────────────────┐
│                         FASTAPI BACKEND                       │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                         API Layer                        │  │
│  │                   /api/v1/chat                          │  │
│  │                   /api/v1/health                        │  │
│  └────────────────────────────┬────────────────────────────┘  │
│                               │                               │
│                               ▼                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                      Chatbot Service                    │  │
│  │                                                         │  │
│  │   Question Processing → RAG Pipeline → Response        │  │
│  └────────────────────────────┬────────────────────────────┘  │
│                               │                               │
│                ┌──────────────┴───────────────┐              │
│                ▼                              ▼              │
│       ┌───────────────────┐          ┌─────────────────────┐  │
│       │   RAG / Retrieval │          │     Gemma LLM       │  │
│       │                   │          │                     │  │
│       │ Embeddings        │          │ Local inference     │  │
│       │ Vector Search     │          │ Ollama/runtime      │  │
│       │ Context Builder   │          │                     │  │
│       └─────────┬─────────┘          └──────────┬──────────┘  │
│                 │                               │             │
│                 ▼                               │             │
│       ┌───────────────────┐                     │             │
│       │    Vector Store   │                     │             │
│       │    Chroma/FAISS   │                     │             │
│       └───────────────────┘                     │             │
│                                                 │             │
│                            ┌────────────────────┘             │
│                            ▼                                  │
│                   Generated Response                          │
└───────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend

| Concern | Technology |
|---|---|
| Language | Python |
| API Framework | FastAPI |
| ASGI Server | Uvicorn |
| Data Validation | Pydantic |
| Local LLM | Gemma |
| Local LLM Runtime | Ollama |
| Embeddings | Sentence Transformers |
| Vector Store | Chroma or FAISS |
| PDF Processing | PyMuPDF |
| Testing | pytest |
| HTTP Testing | httpx |

### Frontend

| Concern | Technology |
|---|---|
| UI | React |
| Language | JavaScript |
| Styling | CSS |
| API Requests | Fetch API or Axios |
| Build Tool | Vite |

> The frontend is intentionally separated from the AI logic. It should communicate with the backend through the API instead of directly interacting with Gemma or the vector database.

---

## 📁 Project Structure

```text
offline-ai-chatbot/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── chat_routes.py
│   │   │       └── health_routes.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   │
│   │   ├── services/
│   │   │   ├── chatbot_service.py
│   │   │   ├── retrieval_service.py
│   │   │   └── generation_service.py
│   │   │
│   │   ├── llm/
│   │   │   ├── gemma_client.py
│   │   │   └── ollama_client.py
│   │   │
│   │   ├── rag/
│   │   │   ├── embeddings.py
│   │   │   ├── retriever.py
│   │   │   ├── prompt_builder.py
│   │   │   └── pipeline.py
│   │   │
│   │   ├── documents/
│   │   │   ├── pdf_parser.py
│   │   │   ├── cleaner.py
│   │   │   ├── chunker.py
│   │   │   └── ingestion.py
│   │   │
│   │   ├── schemas/
│   │   │   └── chat_schema.py
│   │   │
│   │   └── main.py
│   │
│   ├── data/
│   │   ├── raw/
│   │   │   └── educational_materials/
│   │   └── processed/
│   │
│   ├── vector_db/
│   │
│   ├── eval/
│   │   └── test_questions.json
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_chat.py
│   │   ├── test_retrieval.py
│   │   └── test_generation.py
│   │
│   ├── scripts/
│   │   └── build_index.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── public/
│   │
│   └── src/
│       ├── components/
│       │   ├── ChatWindow.jsx
│       │   ├── ChatMessage.jsx
│       │   ├── ChatInput.jsx
│       │   └── LoadingIndicator.jsx
│       │
│       ├── pages/
│       │   └── ChatPage.jsx
│       │
│       ├── services/
│       │   └── chatService.js
│       │
│       ├── hooks/
│       │   └── useChat.js
│       │
│       ├── App.jsx
│       └── main.jsx
│
├── docs/
│   └── architecture.md
│
├── README.md
└── .gitignore
```

---

## 🧠 How the AI Works

The chatbot uses **Retrieval-Augmented Generation (RAG)**.

### Step 1 — Student asks a question

```text
"What causes attenuation in optical fiber?"
```

### Step 2 — Convert the question into an embedding

```text
Question
   ↓
Embedding Model
   ↓
Vector Representation
```

### Step 3 — Search the local vector database

The vector store searches for educational chunks that are semantically similar to the question.

```text
Question Vector
      ↓
Semantic Search
      ↓
Top-K Relevant Chunks
```

### Step 4 — Build the prompt

```text
System Instructions
        +
Retrieved Learning Content
        +
Student Question
        ↓
      Prompt
```

### Step 5 — Generate the answer with Gemma

```text
Prompt
  ↓
Gemma
  ↓
Educational Answer
```

### Step 6 — Return the answer

The backend returns:

- Generated answer
- Relevant source chunks
- Optional metadata

This allows the frontend to display both the answer and where the information came from.

---

## 📚 Knowledge Ingestion Pipeline

Educational documents are prepared before they are used by the chatbot.

```text
PDF / DOCX / TXT
      ↓
Document Loader
      ↓
Text Extraction
      ↓
Cleaning
      ↓
Chunking
      ↓
Embedding Model
      ↓
Vector Database
```

### Example

```text
optical_fiber.pdf
      ↓
Extract text
      ↓
Split into chunks
      ↓
Generate embeddings
      ↓
Store in Chroma/FAISS
```

The stored chunks should retain metadata such as:

```text
subject
topic
document
page
chapter
education_level
```

This makes future filtering and evaluation easier.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Git
- Ollama
- A locally installed Gemma model
- Sufficient RAM/CPU resources for the selected Gemma model

### 1. Clone the repository

```bash
git clone https://github.com/your-username/offline-ai-chatbot.git
cd offline-ai-chatbot
```

### 2. Set up the backend

```bash
cd backend

python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Install and prepare Gemma

Start Ollama and pull the Gemma model you have selected.

Example:

```bash
ollama pull <your-gemma-model>
```

> Model selection depends on the hardware available on the target machine. Do not assume that a specific Gemma size will run efficiently on every computer.

### 4. Configure environment variables

```bash
copy .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

Edit `.env` with your local configuration.

### 5. Add educational materials

Place source documents inside:

```text
backend/data/raw/educational_materials/
```

### 6. Build the vector index

```bash
python -m scripts.build_index
```

### 7. Start FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

API:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

### 8. Start the React frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open the local URL shown by Vite.

---

## 🔐 Environment Variables

Example `.env`:

```env
ENVIRONMENT=development

GEMMA_MODEL_NAME=<your-gemma-model>

OLLAMA_BASE_URL=http://localhost:11434

EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2

VECTOR_STORE_PATH=./vector_db

TOP_K_CHUNKS=5

SIMILARITY_THRESHOLD=0.50
```

> Keep `.env` out of version control when it contains machine-specific or sensitive configuration.

---

## 📡 API Reference

All endpoints are versioned under:

```text
/api/v1/
```

### Health Check

```http
GET /api/v1/health
```

Example response:

```json
{
  "status": "ok"
}
```

### Chat

```http
POST /api/v1/chat
```

Example request:

```json
{
  "question": "What causes attenuation in optical fiber?"
}
```

Example response:

```json
{
  "answer": "Attenuation occurs because optical power decreases as light travels through an optical fiber. Major causes include absorption, scattering, and bending losses.",
  "source_chunks": [
    {
      "document": "optical_fiber.pdf",
      "page": 12
    }
  ]
}
```

---

## 🔎 RAG Engine

The core RAG flow is:

```text
question
   ↓
embed
   ↓
retrieve top-k chunks
   ↓
build grounded prompt
   ↓
Gemma generates answer
```

### Retrieval principles

- Retrieval should happen before generation.
- Retrieved content should be passed explicitly to Gemma.
- The prompt should instruct Gemma to prefer the retrieved content over unsupported assumptions.
- Relevant source chunks should be returned for transparency.
- Subject/topic filtering can be added to reduce irrelevant retrieval.

---

## 🛡️ Hallucination Control

The system should not assume that Gemma is automatically correct.

The RAG layer should therefore support:

```text
Question
   ↓
Retrieve
   ↓
Check relevance
   │
   ├── Relevant → Generate answer
   │
   └── Not relevant → Safe fallback
```

Example fallback:

```text
"I could not find enough relevant information
in the available learning materials to answer
this question reliably."
```

This is preferable to allowing the model to confidently invent an answer.

---

## 🧪 Testing and Evaluation

Run backend tests:

```bash
cd backend
pytest
```

For coverage:

```bash
pytest --cov=. --cov-report=term-missing
```

The evaluation set should contain realistic student questions covering:

- Direct factual questions
- Conceptual questions
- Definition questions
- Why/how questions
- Multi-step questions
- Questions outside the knowledge base
- Ambiguous questions

### Evaluation areas

The chatbot should eventually be evaluated on:

```text
Retrieval Quality
       ↓
Answer Correctness
       ↓
Grounding
       ↓
Hallucination Rate
       ↓
Response Time
       ↓
Offline Reliability
```

---

## 🗺️ Development Roadmap

### Phase 1 — Local Gemma

- [ ] Install Ollama
- [ ] Run selected Gemma model locally
- [ ] Send a question from Python
- [ ] Receive a generated answer
- [ ] Measure response time and resource usage

### Phase 2 — RAG Foundation

- [ ] Collect educational materials
- [ ] Extract text
- [ ] Clean documents
- [ ] Implement chunking
- [ ] Generate embeddings
- [ ] Build vector index
- [ ] Implement semantic retrieval

### Phase 3 — RAG + Gemma

- [ ] Build prompt construction
- [ ] Pass retrieved context to Gemma
- [ ] Add source chunks
- [ ] Add relevance threshold
- [ ] Create evaluation questions
- [ ] Test hallucination behavior

### Phase 4 — Backend

- [ ] Build FastAPI application
- [ ] Add `/health`
- [ ] Add `/chat`
- [ ] Separate routes and services
- [ ] Add validation
- [ ] Add automated tests

### Phase 5 — Frontend

- [ ] Build React chat interface
- [ ] Connect frontend to API
- [ ] Display message history
- [ ] Display retrieved sources
- [ ] Handle loading/error states

### Phase 6 — Local Network

- [ ] Run backend on school server
- [ ] Serve frontend locally
- [ ] Test from multiple devices
- [ ] Test with Internet disconnected
- [ ] Measure concurrent-user performance

### Phase 7 — Future Adaptive Learning Integration

- [ ] Student profiles
- [ ] Quiz system
- [ ] Student performance tracking
- [ ] Mastery estimation
- [ ] Knowledge tracing
- [ ] Adaptive recommendations
- [ ] Personalized AI explanations

---

## 🤝 Contributing

1. Create a feature branch.
2. Keep changes focused.
3. Write tests for new backend functionality.
4. Test the RAG pipeline with realistic student questions.
5. Open a pull request with a clear description of the changes.

### Branch Naming

```text
{scope}-{short-description}
```

Examples:

```text
rag-document-ingestion
rag-vector-retrieval
llm-gemma-integration
api-chat-endpoint
frontend-chat-ui
tests-rag-evaluation
```

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

<p align="center">
  Built offline · Grounded in educational content · Powered by
