# Assure Scanner

## Overview
Assure Scanner is a security compliance tool utilizing RAG (Retrieval-Augmented Generation) to analyze code repositories against compliance frameworks (SOC 2, GDPR, HIPAA, etc.).

## Architecture

This project follows a standard decoupled web architecture:

- **Frontend**: React application with a dashboard for visualization.
- **Backend**: FastAPI (Python) application handling AI logic and orchestration.
- **Database**: PostgreSQL with `pgvector` for storing compliance document embeddings.
- **Message Broker**: Apache Kafka for handling real-time scan events.

## Structure

```
/
├── backend/
│   ├── app/
│   │   ├── main.py          # App entry point
│   │   └── routers/         # API endpoints
│   ├── scripts/             # Data ingestion utilities
│   └── Dockerfile
├── frontend/
│   └── src/components/      # React UI components
├── docs/                    # Architecture references
└── docker-compose.yml       # Local development orchestration
```

## Setup

1. **Environment Variables**: Create a `.env` file with `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `DATABASE_URL`.
2. **Start Services**:
   ```bash
   docker-compose up --build
   ```
3. **Ingest Data** (One-time setup):
   ```bash
   docker-compose exec backend python scripts/ingest_compliance_docs.py
   ```

## Tech Stack
- **AI**: Claude 3.5 Sonnet, OpenAI Embeddings, LangChain
- **Infrastructure**: Docker, Kafka, PostgreSQL (pgvector)