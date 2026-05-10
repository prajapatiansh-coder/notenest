# NoteNest System Design

## Architecture Overview
NoteNest is built on a modular Flask architecture designed for scalability and enterprise readiness.

### Core Components
1.  **Frontend**: Server-side rendered templates using Bootstrap 5 with a custom glassmorphism design system.
2.  **API Layer**: Versioned REST API (v1) using `flask-smorest` and `Marshmallow` for automatic OpenAPI documentation.
3.  **Service Layer**: Business logic is decoupled from route handlers into dedicated services (`NoteService`, `AIService`, `AuthService`).
4.  **Database**: PostgreSQL for relational data with optimized indexing and SQLAlchemy ORM.
5.  **Task Queue**: Celery with Redis as the broker for asynchronous AI processing and background jobs.
6.  **Caching**: Redis-based caching for AI responses and frequently accessed data.
7.  **Real-time**: WebSocket integration via `Flask-SocketIO` for instant notifications and live updates.

## AI & RAG Pipeline
1.  **Text Extraction**: Multi-strategy extraction using `pdfplumber` and `PyPDF2` with `pytesseract` OCR fallback.
2.  **Vector Storage**: Local vector indexing using FAISS for semantic search and context retrieval.
3.  **RAG Orchestration**: Context-aware retrieval for AI chat assistants.

## Multi-tenancy
NoteNest uses a shared database, shared schema approach with `institution_id` discriminators to provide isolated spaces for different colleges/institutions.

## Deployment Stack
- **Web Server**: Gunicorn
- **WSGI/WebSocket**: Eventlet
- **Containerization**: Docker & Docker Compose
- **Monitoring**: Sentry & Prometheus
