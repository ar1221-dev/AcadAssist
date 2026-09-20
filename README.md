# AcadAssist

AcadAssist is an AI-powered study assistant designed to help students organize, understand, practice, and revise their academic material using AI.

## Current Status

Initial project setup.

## Planned Components

- **Azure + Foundry**: Cloud infrastructure, AI models, agents, and Azure AI services integration.
- **Knowledge Base**: Document processing (PDF, PPT, DOCX, TXT), text extraction, chunking, cleaning, metadata, and knowledge base pipelines.
- **Assessment + Planning**: Adaptive quiz generation, difficulty management, history tracking, exam-aware quiz scheduling, daily planner, roadmap, and streak tracking.
- **RAG + Study Intelligence**: Embeddings, vector retrieval, RAG pipeline, context construction, and personalized study analysis.
- **React UI**: Interactive dashboard, navigation, user interface, and integration of backend modules into modern React application (`frontend/`).

## Development Workflow

We follow a structured Git branching strategy:

- `main` &rarr; Stable, production-ready branch. Never commit or push feature work directly to `main`.
- `develop` &rarr; Integration and active development branch. Feature branches merge into `develop` via Pull Requests.
- `feature/*` &rarr; Individual feature branches for specific components and team members.

## Team Structure

| Developer | Component | Responsibilities | Feature Branch |
| :--- | :--- | :--- | :--- |
| **Person 1** | Azure + Foundry | Azure AI services, Microsoft Foundry, AI models, Agents, Cloud infrastructure | `feature/azure-foundry` |
| **Person 2** | Knowledge Base | PDF/PPT/DOCX/TXT processing, text extraction, cleaning, chunking, metadata, pipeline | `feature/knowledge-base` |
| **Person 3** | Assessment + Planning | Quiz system, difficulty levels, question generation, question history/no-repeat logic, exam-aware quiz scheduling, daily planner, roadmap, streak system | `feature/assessment-planning` |
| **Person 4** | RAG + Study Intelligence | Embeddings, vector retrieval, RAG pipeline, context construction, study intelligence, personalized study analysis | `feature/rag-intelligence` |
| **Person 5** | React UI | Modern React frontend (`frontend/`), dashboard, navigation, user interface, design system, backend integration | `react-ui` |

## Setup & Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/ar1221-dev/AcadAssist.git
   cd AcadAssist
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install initial dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Update .env with appropriate local values
   ```
