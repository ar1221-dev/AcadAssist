# AcadAssist — Person 2 Knowledge Base Foundation (Checkpoint 1)

This repository houses the standalone **Knowledge Base & Document-Ingestion Foundation** for AcadAssist (Person 2, Checkpoint 1). It provides end-to-end document management, strict validation, safe storage segregation, automated text extraction across academic formats (PDF, PPTX, PPT, DOCX, DOC, TXT), subject/course categorization, processing pipeline states, and a normalized output interface tailored for downstream RAG (Retrieval-Augmented Generation) by Person 4.

---

## 1. Project Purpose & Scope

The Knowledge Base serves as the ingestion and storage engine for all course materials uploaded by students and educators:
```text
Academic Material (PDF, PPTX, PPT, DOCX, DOC, TXT)
       ↓
Upload & Validation (Type, Size, Empty, Traversal, Duplicate Hash)
       ↓
Segregated Storage (Raw vs. Processed Content)
       ↓
Metadata Management (Subject, Course, Titles, Page/Slide Counts)
       ↓
Document Processing Pipeline (Extraction Engines)
       ↓
Normalized RAG-Ready Content (Deterministic Structure with Boundaries)
       ↓
Clean Interface for Person 4 (RAG / Embeddings / Vector DB)
```

---

## 2. Architecture & Directory Structure

```text
AcadAssist-Person2-KnowledgeBase/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Pydantic Settings (paths, limits, allowed types)
│   ├── main.py                   # FastAPI app, lifespan, CORS, and exception handlers
│   ├── api/
│   │   ├── deps.py               # Dependency injection (DB session, services)
│   │   └── routes/
│   │       └── materials.py      # REST endpoints (/materials, /api/v1/materials)
│   ├── models/
│   │   └── material.py           # SQLAlchemy Material ORM model
│   ├── schemas/
│   │   └── material.py           # Pydantic validation & response schemas
│   ├── services/
│   │   ├── storage.py            # Segregated disk storage manager
│   │   ├── validator.py          # Strict upload and duplicate validation
│   │   ├── knowledge_base.py     # Core orchestrator service
│   │   └── processors/           # Document extraction engines
│   │       ├── base.py           # Base processor & ExtractionResult
│   │       ├── pdf.py            # PDF parser (pypdf)
│   │       ├── pptx.py           # PPTX (python-pptx) & legacy PPT parser
│   │       ├── docx.py           # DOCX (python-docx) & legacy DOC parser
│   │       └── txt.py            # TXT parser with multi-encoding fallback
│   ├── database/
│   │   ├── base.py               # DeclarativeBase
│   │   └── session.py            # SQLite engine, sessionmaker, idempotent table init
│   └── utils/
│       ├── security.py           # Filename sanitization, SHA-256 hash computation
│       └── normalizer.py         # Deterministic text builder for RAG handoff
├── storage/
│   ├── raw/                      # Raw uploaded files: storage/raw/<material_id>/<filename>
│   └── processed/                # Normalized text: storage/processed/<material_id>/content.txt
├── sample_data/                  # Realistic sample documents (PDF, PPTX, PPT, DOCX, DOC, TXT)
├── tests/                        # Full Pytest test suite (30 automated tests)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 3. Supported Document Formats

| Format | Extension | Extractor Engine | Extracted Information |
|---|---|---|---|
| **PDF** | `.pdf` | `pypdf` | Multi-page text, page count, document metadata |
| **PowerPoint** | `.pptx` | `python-pptx` | Slide text frames, tables, speaker notes, slide count |
| **Legacy PPT** | `.ppt` | Binary OLE Stream Extractor | Slide text atoms, UTF-16LE / ASCII text runs |
| **Word** | `.docx` | `python-docx` | Headings, paragraphs, structured tables, core properties |
| **Legacy DOC** | `.doc` | Binary OLE Stream Extractor | WordDocument FIB text chunks, Unicode / ANSI streams |
| **Plain Text** | `.txt` | Multi-Encoding Decoder | UTF-8, UTF-16, Latin-1, CP1252 text with section demarcation |

---

## 4. Setup & Installation

### Prerequisites
- Python 3.11+ (verified up to Python 3.13)
- Windows PowerShell / Linux / macOS terminal

### 1. Clone or Open Directory
```bash
cd /path/to/Person2
```

### 2. Create and Activate Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 5. Running the Application

Start the FastAPI server via Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive OpenAPI Documentation will be live at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 6. REST API Reference

All endpoints are available directly at `/materials` and prefixed at `/api/v1/materials`.

### 1. Upload Material
```http
POST /materials
Content-Type: multipart/form-data
```
**Form Parameters:**
- `file` (File, required): The document file.
- `subject` (string, required): Academic subject (e.g., `Data Structures & Algorithms`).
- `course` (string, optional): Course identifier (e.g., `CS201`).
- `title` (string, optional): Custom title (defaults to filename).
- `description` (string, optional): Document description.

**Response (HTTP 201 Created):**
```json
{
  "id": "c7f07a21-7dd2-4b2a-a9a7-96a1e50587d6",
  "title": "Trees & BST",
  "original_filename": "trees.pdf",
  "filename": "trees.pdf",
  "file_type": "pdf",
  "file_size": 18452,
  "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "subject": "Data Structures",
  "course": "CS201",
  "description": "Lecture 4 Binary Search Trees",
  "processing_status": "PROCESSED",
  "processing_error": null,
  "page_count": 2,
  "slide_count": null,
  "content_length": 450,
  "uploaded_at": "2026-09-20T14:15:00Z",
  "updated_at": "2026-09-20T14:15:01Z"
}
```

### 2. List Materials (with Filtering)
```http
GET /materials?subject=Data Structures&course=CS201&status=PROCESSED&skip=0&limit=50
```
**Response (HTTP 200 OK):**
```json
{
  "total": 1,
  "items": [
    {
      "id": "c7f07a21-7dd2-4b2a-a9a7-96a1e50587d6",
      "title": "Trees & BST",
      "subject": "Data Structures",
      "course": "CS201",
      "file_type": "pdf",
      "processing_status": "PROCESSED",
      "page_count": 2
    }
  ]
}
```

### 3. Get Material Metadata
```http
GET /materials/{material_id}
```

### 4. Get Processed RAG Content
```http
GET /materials/{material_id}/content
```
**Response (HTTP 200 OK):**
```json
{
  "id": "c7f07a21-7dd2-4b2a-a9a7-96a1e50587d6",
  "title": "Trees & BST",
  "subject": "Data Structures",
  "course": "CS201",
  "file_type": "pdf",
  "processing_status": "PROCESSED",
  "content_length": 450,
  "page_count": 2,
  "slide_count": null,
  "processed_content": "=== ACADASSIST KNOWLEDGE BASE METADATA ===\nMaterial ID: c7f07a21...\nTitle: Trees & BST\nSubject: Data Structures\nCourse: CS201\nFile Type: PDF\nNormalized At: 2026-09-20T14:15:01Z\n=== DOCUMENT CONTENT ===\n\n--- Page 1 ---\nData Structures: Binary Search Trees...\n\n--- Page 2 ---\nBST Operations and Complexity..."
}
```

### 5. Get Processing Status
```http
GET /materials/{material_id}/status
```

### 6. Delete Material
```http
DELETE /materials/{material_id}
```
Deletes the database record and permanently wipes both raw file (`storage/raw/{id}`) and processed text (`storage/processed/{id}`) from disk.

---

## 7. Storage Structure

Storage is strictly segregated and accessed through internal UUID identifiers to prevent unauthorized filesystem access:
```text
storage/
├── raw/
│   └── <material_id>/
│       └── sanitized_filename.ext
└── processed/
    └── <material_id>/
        └── content.txt
```
Raw files are preserved in their original binary format for reference, while processed normalized text files are stored in UTF-8 for downstream ingestion.

---

## 8. Security & Validation Controls

- **Directory Traversal Protection**: Rejects file paths containing `..`, `/`, `\`, and null bytes `\x00`.
- **Sanitized Basenames**: Removes shell/path metacharacters, replaces spaces, and enforces a 100-character ceiling.
- **Allowed Extensions**: Whitelist checking (`pdf`, `pptx`, `ppt`, `docx`, `doc`, `txt`).
- **File Size Limits**: Configurable ceiling (`MAX_FILE_SIZE_BYTES`, default 50 MB).
- **Empty File Check**: Files with 0 bytes are rejected immediately with HTTP 400.
- **Duplicate Prevention**: SHA-256 hash calculated upon upload; identical documents under the same subject return HTTP 409 Conflict without silent overwrites.

---

## 9. Future RAG Handoff (Person 4 Interface)

Person 4's RAG and embeddings pipeline can consume materials through two distinct methods without modifying the Knowledge Base:

### Method A: REST API Ingestion
Person 4 calls:
```python
import httpx

# 1. Query materials for a subject
response = httpx.get("http://localhost:8000/materials?subject=Data Structures")
materials = response.json()["items"]

# 2. Retrieve normalized text ready for chunking
for m in materials:
    if m["processing_status"] == "PROCESSED":
        content_data = httpx.get(f"http://localhost:8000/materials/{m['id']}/content").json()
        raw_text = content_data["processed_content"]
        # Person 4 feeds raw_text directly into:
        # text_splitter.split_text(raw_text) -> embeddings -> Chroma/FAISS
```

### Method B: Direct Python Service Access
```python
from app.database.session import SessionLocal
from app.services.knowledge_base import knowledge_base_service

db = SessionLocal()
total, materials = knowledge_base_service.list_materials(db, subject="Data Structures")
for mat in materials:
    content = knowledge_base_service.get_material_content(db, mat.id)
    print(content["processed_content"])
```

### Normalized Content Format
Every processed document follows this exact deterministic structure:
```text
=== ACADASSIST KNOWLEDGE BASE METADATA ===
Material ID: <UUID>
Title: <Title>
Subject: <Subject>
Course: <Course>
File Type: <TYPE>
Normalized At: <ISO Timestamp>
=== DOCUMENT CONTENT ===

--- Page 1 / Slide 1 / Section 1 ---
[Text chunk with preserved boundaries]

--- Page 2 / Slide 2 / Section 2 ---
[Text chunk with preserved boundaries]
```

---

## 10. Automated Tests

The test suite contains 30 automated test cases covering validation, storage, processors, API endpoints, error handling, duplicate prevention, and RAG handoff formatting.

### Run All Tests:
```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\pytest.exe -v
```

### Test Breakdown:
- `tests/test_validators.py`: Filename sanitization, path traversal rejection, empty files, file size limits, duplicate hashing.
- `tests/test_processors.py`: Extraction verification for PDF, PPTX, PPT, DOCX, DOC, TXT, and corrupted document error raising.
- `tests/test_storage.py`: Raw storage, processed storage, disk cleanup upon material deletion.
- `tests/test_rag_handoff.py`: Header and section structure verification for Person 4 RAG compatibility.
- `tests/test_api_materials.py`: Upload, retrieval, subject/course filtering, status polling, deletion, and duplicate rejection.
