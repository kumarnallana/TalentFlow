# TalentFlow

> **Production-ready, asynchronous resume screening and candidate evaluation engine powered by FastAPI and SQLAlchemy.**

TalentFlow streamlines high-volume candidate evaluations by decoupling file uploads, PDF extraction, skill matching, and database persistence into a non-blocking asynchronous pipeline.

---

## Key Features

- **Asynchronous Pipeline**: Decoupled ingestion and background parsing to handle concurrent resume uploads without blocking HTTP workers.
- **Robust State Management**: Built-in state machine tracking each candidate screening job (`queued`, `processing`, `completed`, `failed`).
- **Flexible JSON Payloads**: Leverages PostgreSQL `JSON` columns via SQLAlchemy 2.0 to store dynamic skill lists and structured candidate extractions.
- **Document Ingestion**: Fast extraction of candidate profiles, contact info, and experience from PDF resumes using `pypdf`.
- **Modern Python Architecture**: Built with Python 3.14, SQLAlchemy 2.0 typed `Mapped` columns, dependency-injected database sessions, and managed with `uv`.

---

## Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance asynchronous REST API framework |
| **ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | Strongly-typed SQL toolkit with Declarative Mapped models |
| **Database** | [PostgreSQL](https://www.postgresql.org/) (Supabase) | Relational database with native JSONB support |
| **Driver** | [psycopg 3](https://www.psycopg.org/psycopg3/) | Modern, high-performance PostgreSQL driver for Python |
| **Document Parser**| [pypdf](https://pypdf.readthedocs.io/) | Pure-Python PDF extraction library |
| **Package Manager**| [uv](https://docs.astral.sh/uv/) | Blazing-fast Python package and project manager |

---

## Project Structure

```text
talentflow/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── database.py       # Engine, SessionLocal factory, and Base model
│   ├── models/
│   │   ├── __init__.py
│   │   └── job.py            # JobModel database entity
│   └── main.py               # FastAPI entrypoint and route definitions
├── uploads/                  # Temporary storage for uploaded resumes
├── .agents/
│   └── AGENTS.md             # Project conventions and developer rules
├── .env.example              # Sample environment configuration
├── .gitignore                # Git ignore rules for virtualenvs and secrets
├── pyproject.toml            # Project metadata and dependencies
└── uv.lock                   # Deterministic lockfile
```

---

## Getting Started

### Prerequisites

- Python 3.12+ (or 3.14+)
- [uv](https://docs.astral.sh/uv/) (recommended) or standard `pip`
- PostgreSQL instance (e.g., Supabase, local PostgreSQL, or Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/kumarnallana/TalentFlow.git
cd TalentFlow
```

### 2. Environment Configuration

Create a `.env` file from the provided template:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL database credentials:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/talentflow
```

### 3. Install Dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using standard `pip`:

```bash
pip install -r requirements.txt  # or: uv pip install -e .
```

### 4. Run the Application

```bash
uv run uvicorn app.main:app --reload
```

Once running, interactive API docs will be available at:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## Data Model Overview

### `JobModel` (`jobs` table)

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `VARCHAR` (UUID) | Unique job identifier (Primary Key) |
| `filename` | `VARCHAR` | Original uploaded document name |
| `file_path` | `VARCHAR` | Local / storage path to the uploaded PDF |
| `status` | `VARCHAR(50)` | Current processing status (`queued`, `processing`, etc.) |
| `target_skills` | `JSON` | List of target skills specified for the role |
| `extracted_data` | `JSON` | Extracted profile data, skills, and qualifications |
| `error_message` | `TEXT` | Failure details if processing encounters an error |
| `created_at` | `TIMESTAMP` | UTC creation timestamp |

---

## License

This project is licensed under the MIT License.
