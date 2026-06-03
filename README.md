# Internship Tracker API

![CI](https://github.com/SiddNaiik/internship-tracker-api/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A backend-only REST API for tracking internship applications, built to showcase backend engineering: authentication, relational database modeling, migrations, and API quality.

Designed to simulate real-world backend systems with authentication, relational data modeling, and production-style architecture practices.

> Built to practice production-grade backend patterns — JWT auth, clean routing, strict data modeling, and CI from day one.

## Highlights

- JWT authentication (register/login)
- User-scoped CRUD for:
  - Companies
  - Applications (strict status enum)
- PostgreSQL + Alembic migrations
- Clean FastAPI routing structure (routers/modules)
- Pytest API tests (SQLite in-memory for fast test runs)
- GitHub Actions CI

## Tech Stack

- **FastAPI** — API framework
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **PostgreSQL** — production database (Docker locally / managed in production)
- **Pytest** — test suite (SQLite in-memory)
- **GitHub Actions** — CI

## Data Model

```
users
 └── companies        (user_id → users)
 └── applications     (user_id → users, company_id → companies)
```

Application `status` is a strict enum with the following allowed values:

| Value | Meaning |
|---|---|
| `applied` | Application submitted |
| `interview` | Interview scheduled or completed |
| `offer` | Offer received |
| `rejected` | Application rejected |
| `withdrawn` | Withdrew from the process |

## Project Structure

```
.
├── app/
│   ├── main.py           # App entry point
│   ├── db.py             # DB session setup
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── auth.py           # JWT logic
│   └── api/
│       ├── auth.py       # /auth endpoints
│       ├── companies.py  # /companies endpoints
│       └── applications.py # /applications endpoints
├── alembic/              # Migration files
├── tests/                # Pytest test suite
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── .github/
    └── workflows/
        └── tests.yml
```

## Local Development

### Prerequisites

- Python 3.11+
- Docker + Docker Compose

### 1) Start Postgres

```bash
docker compose up -d
```

This starts PostgreSQL on `localhost:5432` with the database `internship_db`.

### 2) Configure environment

```bash
cp .env.example .env
```

Required variables in `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/internship_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4) Run migrations

```bash
alembic upgrade head
```

### 5) Run the API

```bash
uvicorn app.main:app --reload
```

API docs:
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## API Quickstart (curl)

### Register

```bash
curl -s -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"me@example.com","password":"password123"}'
```

### Login

```bash
curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"me@example.com","password":"password123"}'
```

### Create a company (replace `TOKEN`)

```bash
curl -s -X POST http://127.0.0.1:8000/companies \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"OpenAI","website":"https://openai.com","notes":"Dream company"}'
```

### Create an application

```bash
curl -s -X POST http://127.0.0.1:8000/applications \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"company_id":1,"role_title":"SWE Intern","status":"applied"}'
```

Valid `status` values: `applied`, `interview`, `offer`, `rejected`, `withdrawn`

## Tests

Tests use an in-memory SQLite database — no running Postgres required.

```bash
pytest -q
```

## CI

GitHub Actions runs `pytest` on every push and pull request. See `.github/workflows/ci.yml`.

## Deployment

- Run `alembic upgrade head` on each deploy to apply schema changes
- All resources are user-scoped; JWT tokens are required for every protected route
- Secrets (`SECRET_KEY`, `DATABASE_URL`) should be injected via environment variables — never committed
- Tested against managed PostgreSQL (e.g. Railway, Render, Supabase) — no platform-specific dependencies

## License

MIT