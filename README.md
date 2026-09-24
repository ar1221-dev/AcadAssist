# AcadAssist

**AI-Powered Personalized Academic Study Assistant**

AcadAssist is an intelligent academic companion built to help university students organize course materials, generate grounded summaries, take adaptive practice quizzes, track exam deadlines, and plan daily study sessions with zero-trust security.

---

## Overview

AcadAssist addresses the challenges modern university students face: fragmented course materials across multiple formats, unstructured study schedules, generic AI tools that hallucinate without textbook citations, and a lack of personalized practice targeting specific knowledge gaps.

AcadAssist bridges this gap by providing an end-to-end learning intelligence system:
- **Academic Material Ingestion:** Students upload lecture slides, textbooks, and notes in PDF, PPT, PPTX, DOCX, or TXT formats.
- **Knowledge Base & Semantic Search:** Documents are normalized, chunked, and indexed into a hybrid search engine (BM25 keyword search combined with vector embeddings) ensuring every response is grounded in actual coursework.
- **Adaptive Assessments:** The system generates practice quizzes with configurable question counts (5, 10, 15, or 20 questions) whose difficulty dynamically adapts based on prior performance history.
- **Study Intelligence & Planning:** AcadAssist detects weak topics, tracks upcoming examination dates through multi-tiered proximity windows, and automatically generates prioritized daily study schedules.
- **Grounded Assistant Interaction:** A conversational study assistant answers academic questions with verifiable citations down to the document and page number.

---

## Key Features

### Knowledge Base & Document Processing
- **Multi-Format Ingestion:** Supports `.pdf`, `.ppt`, `.pptx`, `.docx`, and `.txt` files up to 50 MB.
- **Integrity & Deduplication:** Computes SHA-256 checksums on upload to detect and prevent duplicate document storage.
- **Structured Processing Pipeline:** Normalizes text, strips control characters, and segments content into sliding-window chunks (800 characters with 150-character overlap) preserving document, chapter, and page metadata.
- **Centralized Access Control:** Enforces private vs. public document visibility. Private documents remain strictly isolated to their owner.

### Hybrid Retrieval (RAG)
- **Dual Retrieval Engine:** Combines BM25 lexical search with 1536-dimensional vector embeddings for high-recall and high-precision document search.
- **Document-Authoritative Filtering:** When querying against a specific document, stored course and subject metadata remain authoritative, preventing accidental filtering mismatches.
- **Tenant-Level Security Filter:** Every search query enforces a server-side filter `(user_id eq '{user_id}' or visibility eq 'public')`, guaranteeing that unshared student materials are never returned to other users.

### AI Study Assistant
- **Context-Aware Study Chat:** Answers student inquiries with direct references to uploaded course materials.
- **Structured Citations & Actions:** Returns verifiable source citations (document title, filename, page number, relevance score) and actionable next steps (recommended quizzes, flashcard sessions, or revision tasks).
- **Dual Execution Modes:** Connects to Microsoft Foundry / Azure OpenAI deployments in cloud mode, and falls back to a deterministic local orchestrator when running offline or without cloud credentials.

### Assessments & Practice Quizzes
- **Document-Grounded Question Generation:** Quizzes are synthesized directly from retrieved document chunks, avoiding generic or out-of-syllabus questions.
- **Flexible Question Counts:** Supports selectable question counts of 5, 10, 15, or 20 questions per quiz session.
- **Adaptive Difficulty:** Automatically classifies student performance and scales quiz difficulty between `easy`, `medium`, and `hard` based on configurable thresholds (default: < 50% triggers easy/revision, > 75% advances to hard).
- **Automated Grading & Scoring:** Evaluates multiple-choice submissions, computes accuracy percentages, provides answer explanations, and records attempt history.
- **Non-Repeating Question History:** Tracks previously answered questions per user to ensure subsequent quizzes present fresh practice material until the question pool is exhausted.

### Topic Mastery & Progress Tracking
- **Deterministic Topic Analytics:** Aggregates quiz performance to track topic-level accuracy across courses and subjects.
- **Weak Topic Identification:** Automatically flags topics falling below the configurable mastery threshold (< 60%) to prioritize them in future study sessions.
- **Strong Topic Recognition:** Identifies mastered concepts (>= 75% accuracy) to optimize study time toward neglected areas.
- **Course Completion Metrics:** Computes overall course progress percentages based on reading milestones and assessment attempts.

### Study Planning & Exam-Aware Intelligence
- **Optimized Daily Study Schedules:** Generates daily study task lists tailored to available study time (default: 120 minutes/day) and prioritized by weak topics.
- **Exam Countdown Tracking:** Schedules and tracks upcoming course examinations with urgency-based planning adjustments.
- **Proximity Windows:**
  - *Normal (> 14 days):* Balanced pace covering all course modules.
  - *Increased Focus (7–14 days):* Intensified assessment and practice review.
  - *Targeted Weak Topics (3–7 days):* Prioritizes low-mastery concepts and high-yield topics.
  - *Revision Mode (<= 2 days):* Rapid formula, summary, and error-log review.
- **Automated Weekly Reports:** Generates weekly study summaries detailing total hours invested, concepts mastered, quizzes completed, and active study streaks.

### System & Cloud Diagnostics
- **Lightweight Health Probes:** Exposes `/api/health` and `/api/health/azure` for read-only connectivity verification.
- **Zero-Secret Leakage:** Diagnostic checks sanitize internal errors and never return passwords, tokens, API keys, or connection strings in HTTP responses.
- **Live Cloud Status UI:** Integrated **Settings -> System Diagnostics & Cloud Status** view in the frontend provides real-time service indicators.

---

## How AcadAssist Works

```text
Student
   │
   ▼
React Frontend (TypeScript / Vite / Tailwind CSS)
   │
   │ Authenticated HTTP / JWT Bearer Requests (No client-supplied user_id)
   ▼
FastAPI Backend (app/main.py)
   │
   ├── Core Security: get_current_user Dependency (Server-derived identity)
   │
   ├── Knowledge & Document Pipeline
   │     ├─ File Validation (ext, size, SHA-256 deduplication)
   │     ├─ Text Extraction & Normalization (PDF, PPTX, DOCX, TXT)
   │     ├─ Chunking (800 chars / 150 overlap) & 1536-dim Embeddings
   │     └─ Storage (Local filesystem or Azure Blob Storage)
   │
   ├── Hybrid Retrieval & Search
   │     ├─ In-memory LocalHybridSearchIndex (BM25 + Cosine) OR Azure AI Search
   │     └─ Mandatory Security Filter: (user_id eq '{user_id}' or visibility eq 'public')
   │
   ├── Assessment Subsystem
   │     ├─ Document-Authoritative Quiz Generator (5 / 10 / 15 / 20 questions)
   │     ├─ Adaptive Difficulty Engine (easy / medium / hard)
   │     └─ Automated Grading, History Tracking & Non-Repeating Question Pool
   │
   ├── Study Intelligence & Planner
   │     ├─ Weak Topic Detection (< 60% accuracy)
   │     ├─ Exam Proximity Scheduler (Normal / 7-day / 3-day / Revision)
   │     └─ Daily Study Plans & Weekly Learning Reports
   │
   └── AcadAssist Agent Orchestrator (app/azure/agent.py)
         ├─ Cloud Mode: Microsoft Foundry / Azure OpenAI + 11 Academic Tools
         └─ Local Mode: Deterministic Local Orchestrator Fallback
```

---

## Architecture

### Frontend
- **Framework:** React 19 with TypeScript (~6.0) and Vite 8.
- **Styling:** Tailwind CSS v4 with curated dark/light design system tokens.
- **Component Ecosystem:** Lucide React icons, Framer Motion transitions, and Recharts data visualizations.
- **State & Context:**
  - `AuthContext`: Centralized JWT token handling, profile loading, and logout cleanup.
  - `AppContext`: Real-time stats, subjects, exams, notifications, and material store.
- **Key Views:**
  - `Dashboard`: Daily stats, recommendations, urgent deadlines, and study streaks.
  - `Assistant`: Interactive chat with citation inspection and suggested action execution.
  - `Knowledge`: Document repository, upload modal, processing status, and summary viewer.
  - `Assessment`: Practice quiz builder (5/10/15/20 questions), timed test interface, and score reports.
  - `Planner`: Calendar views (Month, Week, Day), task manager, and focus timer.
  - `Progress`: Topic mastery radar, study time trends, and weekly report generator.
  - `Settings`: User profile settings and live System Diagnostics & Cloud Status panel.

### Backend
- **Framework:** FastAPI 0.110+ on Python 3.11+.
- **Validation:** Pydantic v2 and `pydantic-settings`.
- **Database Layer:** SQLAlchemy 2.0 ORM with connection pooling.
- **Route Organization:**
  - `/api/auth`: Registration, login, profile, and logout.
  - `/api/health`: Application status and safe Azure cloud diagnostics.
  - `/api/documents`: Ingestion, metadata, downloads, visibility toggling, and processing.
  - `/api/knowledge`: Hybrid knowledge retrieval for student queries.
  - `/api/chat`: Grounded conversational agent with message history.
  - `/api/quizzes`: Adaptive quiz generation, retrieval, and automated scoring.
  - `/api/performance`: Topic mastery analytics and weak topic detection.
  - `/api/exams`: Examination schedule management and upcoming deadline queries.
  - `/api/plans` & `/api/tasks`: Daily study schedule generation and task status tracking.
  - `/api/reports`: Weekly learning summary generation and retrieval.
  - `/api/tools/*`: 11 typed tool endpoints for Microsoft Foundry agent integration.

### Data & Storage
- **Database:** Local SQLite (`./data/acadassist.db`) for development; configurable to PostgreSQL via `DATABASE_URL`.
- **Binary Storage:** Local filesystem (`./data/storage`) by default. Configurable to Azure Blob Storage using private containers and short-lived SAS tokens.
- **Search & Retrieval:** Local in-memory hybrid search index (BM25 + cosine similarity) by default. Configurable to Azure AI Search.
- **Embeddings:** Local deterministic 1536-dimensional hash provider by default. Configurable to Azure OpenAI (`text-embedding-3-small`).
- **Cloud Independence:** The application functions fully offline without active Azure credentials.

### AI & Retrieval Augmented Generation (RAG)
- **Chunking Strategy:** Sliding-window character chunking (800 characters with 150-character overlap) preserves context across page boundaries.
- **Embedding Dimensions:** 1536 dimensions across both local deterministic provider and cloud models.
- **Prompt Grounding:** Prompts inject retrieved chunks with document title, filename, and page references, instructing the LLM to strictly decline answering if facts are absent from the material.
- **Foundry Boundary:** The 11 academic tools are formally defined in `foundry_openapi.json` and implemented via `ToolDispatcher` in `app/azure/adapters.py`.

---

## Project Structure

```text
AcadAssist/
├── app/                              # FastAPI backend application
│   ├── api/                          # REST API routes and tool endpoints
│   │   ├── routes/                   # Endpoint routers (auth, docs, chat, plans, health, etc.)
│   │   └── tools.py                  # 11 Microsoft Foundry tool HTTP endpoints
│   ├── assessment/                   # Person 3: Assessment & Quiz Subsystem
│   │   ├── api/                      # Quiz, performance, and exam routers
│   │   ├── models.py                 # Quiz, Question, and Attempt ORM models
│   │   ├── schemas.py                # Assessment Pydantic validation schemas
│   │   └── services/                 # Quiz generation, adaptive difficulty, scoring
│   ├── azure/                        # Person 1: Azure Infrastructure & Foundry Agent
│   │   ├── adapters.py               # Subsystem tool adapters & ToolDispatcher
│   │   ├── agent.py                  # AcadAssistAgentService orchestrator
│   │   ├── credentials.py            # Azure Entra ID credential resolver
│   │   ├── foundry.py                # Microsoft Foundry Project manager
│   │   ├── search.py                 # Azure AI Search manager
│   │   ├── storage.py                # Azure Blob Storage client
│   │   └── tools.py                  # Agent tool definitions and schemas
│   ├── core/                         # Core infrastructure utilities
│   │   ├── auth.py                   # Server-derived get_current_user dependency
│   │   ├── database.py               # Database session dependency
│   │   └── security.py               # JWT encoding/decoding and bcrypt password hashing
│   ├── database/                     # SQLAlchemy session and model metadata
│   ├── models/                       # Shared entity models (User, Document, Chunk, Note, Plan)
│   ├── schemas/                      # Shared Pydantic request/response schemas
│   ├── services/                     # Business logic (processing, RAG, study intelligence)
│   ├── config.py                     # Unified Pydantic settings with .env loading
│   └── main.py                       # FastAPI application factory and lifespan setup
├── config/                           # Application configuration helpers
├── docs/                             # Technical subsystem documentation
├── frontend/                         # React 19 + TypeScript + Vite web client
│   ├── src/
│   │   ├── components/               # Navbar, Sidebar, and shared UI elements
│   │   ├── context/                  # AuthContext and AppContext state providers
│   │   ├── pages/                    # Subsystem page components
│   │   ├── services/                 # API client, auth service, and storage helpers
│   │   ├── App.tsx                   # Main router and view layout
│   │   └── index.css                 # Design system styles and Tailwind directives
│   ├── package.json                  # Frontend scripts and dependencies
│   └── vite.config.ts                # Vite configuration
├── tests/                            # Comprehensive pytest test suite (141 tests)
├── .env.example                      # Template for environment configuration
├── foundry_openapi.json              # OpenAPI 3.0 specification for Microsoft Foundry
├── pytest.ini                        # Pytest configuration
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## Core Modules

| Module | Location | Primary Responsibilities |
| :--- | :--- | :--- |
| **Authentication & Security** | `app/core/auth.py`<br>`app/core/security.py`<br>`app/api/routes/auth.py` | JWT token generation and verification (HS256), bcrypt password hashing, `get_current_user` server-derived identity resolution, and user registration/login. |
| **Document Processing** | `app/services/processing/`<br>`app/api/routes/documents.py` | Multi-format parsing (PDF, PPTX, DOCX, TXT), SHA-256 deduplication, text normalization, sliding-window chunking, and document access validation. |
| **RAG & Hybrid Search** | `app/services/rag/search.py`<br>`app/services/rag/knowledge.py` | Dual search implementation: `LocalHybridSearchIndex` (in-memory BM25 + cosine) and `AzureSearchService` with user isolation filtering. |
| **Agent Orchestrator** | `app/azure/agent.py`<br>`app/azure/foundry.py` | Central `AcadAssistAgentService` coordinating LLM interactions via Microsoft Foundry Project or local deterministic orchestrator fallback. |
| **Tool Dispatcher** | `app/azure/adapters.py`<br>`app/api/tools.py` | Bridges LLM tool invocations to backend subsystem methods across Knowledge Base, Assessment, and Study Intelligence. Strictly enforces authenticated `user_id`. |
| **Assessment Engine** | `app/assessment/services/` | Document-authoritative quiz generation (5–20 questions), dynamic difficulty scaling (`easy`, `medium`, `hard`), automated scoring, and non-repeating question pools. |
| **Study Intelligence** | `app/services/planner.py`<br>`app/services/progress.py`<br>`app/services/reports.py` | Weak topic identification (< 60%), exam countdown tracking with proximity rules, daily study schedule creation, and weekly progress reporting. |
| **System Diagnostics** | `app/api/routes/health.py` | Safe, read-only health and cloud diagnostic probes (`/api/health`, `/api/health/azure`) distinguishing 6 distinct connectivity states without exposing credentials. |
| **Frontend Client** | `frontend/src/` | Responsive React UI providing specialized dashboard, chat assistant, document repository, quiz player, study planner, and cloud diagnostics views. |

---

## API

All API endpoints are prefixed with `/api` unless otherwise noted. Protected endpoints strictly require a valid JWT Bearer token in the `Authorization` header (`Bearer <token>`).

### Authentication
| Method | Path | Purpose | Authentication |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register a new student account with hashed password | Public |
| `POST` | `/api/auth/login` | Authenticate credentials and receive JWT access token | Public |
| `GET` | `/api/auth/me` | Retrieve profile of currently authenticated user | Bearer Token |
| `POST` | `/api/auth/logout` | Acknowledge session termination | Bearer Token |

### System & Health Diagnostics
| Method | Path | Purpose | Authentication |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` or `/api/health` | Unified system readiness and subsystem operational status | Public |
| `GET` | `/api/health/azure` | Read-only connectivity diagnostics for Azure services | Public |
| `GET` | `/` | Root greeting with documentation and frontend links | Public |

### Knowledge Base & Documents
| Method | Path | Purpose | Authentication |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/documents` | Upload, deduplicate, and record an academic document | Bearer Token |
| `GET` | `/api/documents` | List documents owned by user or marked as public | Bearer Token |
| `GET` | `/api/documents/{id}` | Retrieve document metadata with ownership verification | Bearer Token |
| `GET` | `/api/documents/{id}/download` | Securely stream binary document file content | Bearer Token |
| `PATCH` | `/api/documents/{id}/visibility` | Update document visibility (`private` vs. `public`) | Bearer Token |
| `POST` | `/api/documents/{id}/process` | Trigger parsing, chunking, and search indexing | Bearer Token |
| `POST` | `/api/documents/{id}/summarize` | Generate structured summary from document chunks | Bearer Token |
| `DELETE` | `/api/documents/{id}` | Delete document from storage, search index, and database | Bearer Token |
| `POST` | `/api/knowledge/search` | Search indexed course materials using hybrid retrieval | Bearer Token |

### Assistant & Chat
| Method | Path | Purpose | Authentication |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/chat` | Send message to AcadAssist Agent and receive grounded response | Bearer Token |
| `GET` | `/api/chat/history` | Retrieve user's historical chat messages | Bearer Token |
| `POST` | `/api/chat/message` | Persist a user or assistant message to chat history | Bearer Token |

### Assessment & Practice Quizzes
| Method | Path | Purpose | Authentication |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/quizzes` | Generate adaptive quiz grounded in course documents | Bearer Token |
| `GET` | `/api/quizzes/{id}` | Retrieve generated quiz questions (without answers) | Bearer Token |
| `POST` | `/api/quizzes/{id}/submit` | Submit answers, calculate score, and record history | Bearer Token |
| `GET` | `/api/quizzes/attempts` | List past quiz attempts and scores for authenticated user | Bearer Token |
| `GET` | `/api/performance` | Retrieve historical performance metrics and topic mastery | Bearer Token |
| `GET` | `/api/performance/weak-topics` | Retrieve detected weak topics requiring practice | Bearer Token |
| `POST` | `/api/exams` | Schedule a new academic examination | Bearer Token |
| `GET` | `/api/exams` | List all exams scheduled by authenticated user | Bearer Token |
| `GET` | `/api/exams/upcoming` | List future upcoming exams sorted by date | Bearer Token |

### Study Intelligence & Planning
| Method | Path | Purpose | Authentication |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/progress` | Retrieve course completion percentages and milestones | Bearer Token |
| `GET` | `/api/progress/recommendations` | Retrieve actionable, deterministic study recommendations | Bearer Token |
| `POST` | `/api/plans` | Generate an exam-aware daily study plan | Bearer Token |
| `GET` | `/api/plans` | List all saved study plans for authenticated user | Bearer Token |
| `GET` | `/api/plans/today` | Retrieve today's scheduled study sessions and tasks | Bearer Token |
| `GET` | `/api/tasks` | List study tasks for authenticated user | Bearer Token |
| `POST` | `/api/tasks` | Create a new study task | Bearer Token |
| `PATCH` | `/api/tasks/{id}` | Update study task completion status | Bearer Token |
| `DELETE` | `/api/tasks/{id}` | Delete a study task | Bearer Token |
| `POST` | `/api/reports/weekly` | Generate and store a weekly study progress summary | Bearer Token |
| `GET` | `/api/reports/weekly` | Retrieve historical weekly study progress reports | Bearer Token |

### Notes
| Method | Path | Purpose | Authentication |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/notes` | List study notes created by authenticated user | Bearer Token |
| `POST` | `/api/notes` | Create a new study note linked to course or topic | Bearer Token |
| `PATCH` | `/api/notes/{id}` | Update note title, content, or subject | Bearer Token |
| `DELETE` | `/api/notes/{id}` | Delete note owned by authenticated user | Bearer Token |

### Microsoft Foundry Tools (`/api/tools/*`)
These endpoints expose the 11 typed tools registered in `foundry_openapi.json`:
- `POST /api/tools/search_knowledge` — Search indexed course materials.
- `POST /api/tools/summarize_document` — Generate grounded document summary.
- `POST /api/tools/generate_quiz` — Generate an adaptive practice quiz.
- `POST /api/tools/submit_quiz` — Submit quiz answers and update mastery.
- `POST /api/tools/get_performance` — Retrieve student performance metrics.
- `POST /api/tools/get_weak_topics` — Identify student weak topics.
- `POST /api/tools/get_progress` — Retrieve course completion progress.
- `POST /api/tools/get_upcoming_exams` — Retrieve upcoming exams and deadlines.
- `POST /api/tools/create_study_plan` — Create an optimized study plan.
- `POST /api/tools/get_today_plan` — Retrieve today's study schedule.
- `POST /api/tools/generate_weekly_report` — Generate a weekly learning summary.

---

## System & Cloud Diagnostics

AcadAssist includes built-in diagnostic endpoints designed to report subsystem and cloud service connectivity safely:

### 1. Unified Application Health (`GET /api/health` and `GET /health`)
Returns the general application health state, database connectivity status, and operational readiness for all three subsystems:
```json
{
  "status": "healthy",
  "service": "AcadAssist API",
  "environment": "development",
  "app": "AcadAssist",
  "version": "2.0.0",
  "database": "connected",
  "subsystems": {
    "knowledge_rag": "operational",
    "assessment": "operational",
    "study_intelligence": "operational"
  },
  "foundry": { "mode": "local_orchestrator", "configured": false },
  "azure_storage": { "mode": "local_storage", "configured": false },
  "azure_search": { "mode": "local_hybrid_index", "configured": false },
  "embeddings": { "mode": "local_deterministic", "configured": false, "model": "text-embedding-3-small", "dimensions": 1536 }
}
```

### 2. Azure Cloud Diagnostics (`GET /api/health/azure`)
Performs lightweight, read-only connectivity checks against Azure Blob Storage, Azure AI Search, and Microsoft Foundry.

Each service reports one of six distinct statuses:
- **`not_configured`**: Service credentials or endpoints are omitted. Local fallback is actively serving requests.
- **`connected`**: A lightweight read-only check confirmed successful service communication (e.g. container existence probe, index list probe, or model deployment list).
- **`authentication_failed`**: The service rejected credentials (invalid API key, expired token, or Entra ID authorization failure).
- **`unreachable`**: Network timeout, DNS resolution failure, or blocked firewall port.
- **`error`**: An unexpected service error response was received.
- **`not_implemented`**: The required Azure SDK package is not installed.

#### Safe Read-Only Design
- **Zero Credential Exposure:** Diagnostic outputs NEVER return API keys, connection strings, JWT secrets, or authorization headers.
- **Sanitized Messages:** Underlying exception strings are sanitized to prevent internal cloud infrastructure details from leaking to clients.

---

## Azure & Microsoft Foundry Configuration

AcadAssist runs out-of-the-box in local mode. Configuring Azure cloud services is strictly optional.

### Environment Variables
Environment variables are configured in `.env` (copied from `.env.example`).

```env
# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=True
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
JWT_SECRET_KEY=change_this_to_a_secure_random_32_byte_secret_in_production

# Database (Default: local SQLite database)
DATABASE_URL=sqlite:///./data/acadassist.db

# Azure Storage (Optional)
AZURE_STORAGE_ACCOUNT=
AZURE_STORAGE_CONNECTION_STRING=
AZURE_STORAGE_CONTAINER=acadassist-documents
STORAGE_LOCAL_DIR=./data/storage

# Azure AI Search (Optional)
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_KEY=
AZURE_SEARCH_INDEX=acadassist-index

# Microsoft Foundry Project (Optional)
FOUNDRY_PROJECT_ENDPOINT=
FOUNDRY_PROJECT=acadassist-foundry
FOUNDRY_MODEL_DEPLOYMENT=gpt-4.1-mini
FOUNDRY_EMBEDDING_DEPLOYMENT=text-embedding-3-small
FOUNDRY_AGENT_NAME=AcadAssist

# Direct Azure OpenAI or OpenAI (Optional Alternative to Foundry Project Endpoint)
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
OPENAI_API_KEY=
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
```

### Authentication Priority for LLM & Foundry
The `FoundryProjectManager` supports three independent authentication paths:
1. **Direct Azure OpenAI:** Set `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`.
2. **Direct OpenAI:** Set `OPENAI_API_KEY`.
3. **Microsoft Foundry Project:** Set `FOUNDRY_PROJECT_ENDPOINT` and authenticate via Entra ID (`DefaultAzureCredential`).

### Unconfigured / Offline Behavior
If cloud variables are omitted or left blank:
- Documents are saved to `STORAGE_LOCAL_DIR` (`./data/storage`).
- Search uses the in-memory `LocalHybridSearchIndex` (BM25 + cosine similarity).
- Embeddings are generated deterministically by `LocalDeterministicEmbeddingProvider`.
- Assistant chat and quiz generation run via the local test orchestrator.

---

## Installation

### Prerequisites
- **Python:** 3.11 or later
- **Node.js:** 18.0 or later (v20+ recommended)
- **npm:** 9.0 or later
- **Git**
- *Azure Subscription (Optional):* Required only if enabling cloud Blob Storage, AI Search, or Foundry.

### 1. Clone Repository

```bash
git clone https://github.com/ar1221-dev/AcadAssist.git
cd AcadAssist
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Windows (PowerShell):
Copy-Item .env.example .env

# Linux / macOS:
cp .env.example .env
```

Open `.env` and review settings. The default configuration connects to local SQLite and local storage paths without requiring Azure credentials.

### 4. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

---

## Running the Application

### 1. Start Backend Development Server

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- API Base URL: `http://127.0.0.1:8000`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc UI: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
- Health Endpoint: `http://127.0.0.1:8000/api/health`

### 2. Start Frontend Development Server

Open a second terminal:

```bash
cd frontend
npm run dev
```

- Web Application URL: `http://localhost:5173`

---

## Testing

AcadAssist maintains automated test suites covering authentication, access isolation, document processing, RAG search, adaptive quizzes, and cloud diagnostics.

### Backend Tests

```bash
# Run full test suite (141 tests)
python -m pytest -q

# Run specific security isolation tests
python -m pytest tests/test_person1_security.py -v

# Run health and Azure diagnostics tests
python -m pytest tests/test_health_and_azure_diagnostics.py -v
```

### Frontend Checks

```bash
cd frontend

# Run code linter (oxlint)
npm run lint

# Run TypeScript compilation and production build
npm run build
```

---

## Authentication

AcadAssist implements zero-trust authentication to protect student coursework and performance data:

1. **User Registration (`POST /api/auth/register`):**
   - Validates student email format and password strength (minimum 8 characters).
   - Generates a bcrypt password hash with salt; plain passwords are never stored.
   - Issues a signed JSON Web Token (JWT) with user ID (`sub`) and email claims.
2. **User Login (`POST /api/auth/login`):**
   - Validates credentials against stored bcrypt hash.
   - Issues a fresh HS256 JWT access token.
3. **Authenticated Requests:**
   - The React client passes the token via `Authorization: Bearer <token>`.
   - The backend `get_current_user` dependency decodes the token, verifies signatures, and resolves the trusted `User` model from the database.
4. **Server-Derived Identity:**
   - Client endpoints never accept a client-chosen `user_id` as authoritative. If a client transmits a mismatched `user_id`, the backend rejects the request with `HTTP 403 Forbidden`.
5. **Anti-Impersonation in Tools:**
   - When the LLM calls internal tools, the `ToolDispatcher` unconditionally overrides any model-generated `user_id` parameter with the authenticated identity.
6. **Session Logout (`POST /api/auth/logout`):**
   - Clears tokens from browser `localStorage` and terminates client sessions.

---

## Data & Storage Model

AcadAssist provides dual-mode data handling, allowing local development while remaining production-ready for Azure:

| Data Type | Current / Local Handling | Optional Azure / Cloud Configuration |
| :--- | :--- | :--- |
| **Relational Data**<br>(Users, Courses, Subjects, Plans, Exams, Quiz Attempts) | SQLite database (`./data/acadassist.db`) | PostgreSQL via `DATABASE_URL` |
| **Document Binaries**<br>(Uploaded PDF, PPTX, DOCX, TXT files) | Local disk storage (`./data/storage/`) | Azure Blob Storage private container with SAS URLs (`AZURE_STORAGE_CONTAINER`) |
| **Document Chunks & Index**<br>(Normalized text segments, metadata) | In-memory `LocalHybridSearchIndex`<br>(BM25 + Cosine similarity) | Azure AI Search service index (`AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_INDEX`) |
| **Vector Embeddings**<br>(1536-dimensional vectors) | `LocalDeterministicEmbeddingProvider`<br>(Reproducible hash embeddings) | Azure OpenAI Service (`text-embedding-3-small`) |
| **AI Study Assistant**<br>(Chat reasoning, quiz synthesis) | Deterministic `local_orchestrator` | Microsoft Foundry / Azure OpenAI (`gpt-4.1-mini`) |

---

## Security

- **Server-Derived Identity:** All sensitive operations derive user identity from verified JWT tokens. Client requests cannot act on behalf of another user.
- **Document & Chunk Isolation:** Document retrieval, downloads, and search chunk queries enforce ownership or explicit public visibility: `(user_id eq '{user_id}' or visibility eq 'public')`.
- **Visibility Synchronization:** Changing a document's visibility between `private` and `public` updates both the database records and all corresponding search index chunks.
- **Environment Isolation:** Secrets, keys, and tokens are loaded strictly via environment variables. The `.env` file is excluded from Git via `.gitignore`.
- **Safe Diagnostics:** Diagnostic endpoints sanitize error outputs to prevent sensitive connection strings, account keys, or stack traces from reaching clients.
- **Safe Production Validation:** When `ENVIRONMENT=production`, the application validates that required Azure credentials and non-wildcard CORS configurations are present at startup.

---

## Development Workflow

1. **Create a Feature Branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Implement Changes:**
   - Maintain subsystem separation (Knowledge Base, Assessment, Study Intelligence, Azure).
   - Enforce server-derived authentication on new endpoints.
   - Keep local fallbacks functional when adding cloud features.
3. **Verify Locally:**
   ```bash
   # Run backend tests
   python -m pytest -q

   # Run frontend lint and build
   cd frontend
   npm run lint
   npm run build
   cd ..
   ```
4. **Review Git Status:**
   ```bash
   git status
   git diff
   ```
5. **Commit and Open Pull Request:**
   ```bash
   git commit -m "feat: description of changes"
   git push origin feature/your-feature-name
   ```

---

## Troubleshooting

### Backend Fails to Start
- **Symptom:** `ModuleNotFoundError: No module named 'fastapi'` (or similar).
- **Fix:** Activate virtual environment (`.\.venv\Scripts\Activate.ps1` or `source .venv/bin/activate`) and run `pip install -r requirements.txt`.

### Port Already in Use
- **Symptom:** `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`.
- **Fix:** Terminate existing process on port 8000:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
  ```
  Or run uvicorn on an alternate port: `--port 8001`.

### Azure Services Report `not_configured`
- **Symptom:** `GET /api/health/azure` returns `"status": "not_configured"`.
- **Explanation:** This is expected when running locally without Azure credentials. Local file storage, in-memory search, and the local agent orchestrator are actively serving requests.

### Azure Services Report `authentication_failed`
- **Symptom:** `GET /api/health/azure` returns `"status": "authentication_failed"`.
- **Fix:** Verify `AZURE_STORAGE_CONNECTION_STRING`, `AZURE_SEARCH_KEY`, or `AZURE_OPENAI_API_KEY` in `.env`. Ensure your Entra ID credentials have the required Role-Based Access Control (RBAC) roles (e.g. *Storage Blob Data Contributor*, *Search Index Data Reader*).

### Azure Services Report `unreachable`
- **Symptom:** `GET /api/health/azure` returns `"status": "unreachable"`.
- **Fix:** Check internet connectivity, corporate proxy settings, and verify that the endpoint URLs in `.env` (such as `AZURE_SEARCH_ENDPOINT`) are typed correctly without trailing slashes.

### Frontend Dependency or Build Issues
- **Symptom:** `npm run build` reports module errors or Vite failures.
- **Fix:** Delete `node_modules` and re-install:
  ```bash
  cd frontend
  rm -rf node_modules package-lock.json
  npm install
  npm run build
  ```

---

## API Documentation

When the backend is running, interactive API documentation is available at:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI Schema:** [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)
- **Microsoft Foundry Tools Specification:** `foundry_openapi.json` in repository root.

---

## Current Project Status

The final AcadAssist implementation has been integrated and verified:
- **Unified Architecture:** Consolidated Knowledge Base (RAG), Assessment, and Study Intelligence subsystems into a unified FastAPI backend and React frontend.
- **Test Suite Coverage:** 141 backend automated test cases covering authentication, document processing, adaptive quizzes, exam scheduling, and Azure diagnostics.
- **Frontend Code Quality:** `oxlint` passes with 0 errors; production bundle builds cleanly via Vite (`tsc -b && vite build`).
- **Grounded Assessments:** Document-authoritative quiz generation verified with selectable question counts (5, 10, 15, 20) and non-repeating question history.
- **Diagnostics Verified:** Live health and cloud diagnostic endpoints tested across all connectivity states without secret leakage.

---

## Future Improvements

The following items represent potential future enhancements:
- **Extended Analytics:** Spaced repetition scheduling (SuperMemo/Anki algorithms) and long-term memory retention forecasting.
- **Expanded Document Support:** Ingestion of EPUB ebooks, Jupyter notebooks (`.ipynb`), Markdown files, and audio lecture transcriptions.
- **Advanced Cloud Observability:** OpenTelemetry tracing, Azure Application Insights integration, and structured Prometheus metrics.
- **Containerization & CI/CD:** Docker multi-stage build workflows and automated GitHub Actions test matrices.
- **Multi-Model LLM Providers:** Modular provider adapters for alternative inference engines (Anthropic Claude, Google Gemini).
