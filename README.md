# CV Ranking System

AI-powered CV generation and ranking system using Gemini LLM, ChromaDB vector search, and RAG evaluation.

## Architecture

For simplicity the two services are logically separated but exist in the same server;
this allows for less code, simpler architecture and they can share the candidates with sqlite. It was not meant to show production readiness but focus on the vector/RAG implementation.

- **Service 1 (POST /api/generate-cvs)**: Makes 3 concurrent Gemini API calls to generate 60 realistic CV archetypes, then multiplies them to 600 unique candidates using Faker. Stores all records in SQLite. Takes 20-30 seconds.
- **Service 2 (POST /api/rank-cvs)**: Vectorizes all 600 candidate summaries into ChromaDB, performs cosine similarity search for the top 5 matches, then sends them through a RAG evaluation step via Gemini for detailed scoring. Takes 20-30 seconds.


## Tech Stack

| Layer    | Technology                                |
|----------|-------------------------------------------|
| Backend  | Python 3.11, FastAPI, SQLite, ChromaDB    |
| LLM      | Google Gemini 2.5 Flash (via google-genai)|
| Frontend | React, Vite, TypeScript, Tailwind CSS     |
| Infra    | Docker, Docker Compose                    |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- A Gemini API key (free tier works)

### Run

```bash
# 1. Clone and enter the project
cd cv-ranking-system

# 2. Set your Gemini API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY (required)

# 3. Build and start
docker-compose up --build
```

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Health check**: http://localhost:8000/api/health

### Usage

1. Make sure `GEMINI_API_KEY` is set in your `.env` file.
2. Paste a job description into the sidebar textarea.
3. Click **Generate Candidates** — generates 600 CVs (~30s).
4. Click **Rank Candidates** — returns the top 5 with scores, pros, and cons.

## Project Structure

```
cv-ranking-system/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       ├── models.py
│       ├── services/
│       │   ├── generator.py    # Service 1
│       │   └── ranker.py       # Service 2
│       └── routers/
│           ├── generate.py
│           └── rank.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    └── src/
        ├── App.tsx
        ├── api.ts
        └── components/
            ├── Sidebar.tsx
            └── ResultsTable.tsx
```
