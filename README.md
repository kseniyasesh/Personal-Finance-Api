# 💰 Personal Finance API

REST API for personal finance tracking built with FastAPI and PostgreSQL.

> This project was implemented as part of a practical track on the [Solvit](https://solvit.space/projects/personal_finance_tracker) platform.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL 15
- SQLAlchemy 2.0 (async)
- Alembic
- Pydantic V2
- JWT Authentication
- Docker & Nginx

## Project Structure

```
app/
├── main.py               # Entry point and configuration
├── database.py           # DB connection and session management
├── models.py             # SQLAlchemy models
├── schemas.py            # Pydantic schemas
├── security.py           # JWT, hashing, and tokens
└── routers/              # Module-based routers
    ├── categories.py     # Categories
    ├── transactions.py   # Transactions (ACID, Filters)
    └── reports.py        # Analytics and reports
migrations/               # Database migration history
tests/                    # Automated tests (Pytest)
```

## Quick Start

### With Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com
cd Personal-Finance-Api

# Create .env file
cp .env.example .env

# Start containers
docker-compose up --build -d

# Apply migrations
docker-compose exec app alembic upgrade head
```

The API will be available at: http://localhost:8000
Swagger UI: http://localhost:8000/docs

### Locally (Without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication


| Method | Endpoint | Description |
|-------|----------|----------|
| POST | /auth/login | Login (Obtain Access and Refresh tokens) |

### Transactions


| Method | Endpoint | Description | Access |
|-------|----------|----------|--------|
| GET | /transactions/ | List of operations (pagination, filters) | All |
| POST | /transactions/ | Add an operation (ACID protection) | All |
| GET | /transactions/report | Quick report by categories | All |

### Analytics (Reports)


| Method | Endpoint | Description |
|-------|----------|----------|
| GET | /reports/categories | Summary of spending by category |
| GET | /reports/timeseries | Expense dynamics by day |
| GET | /reports/budgets/progress | Budget limit status |

## Usage Examples

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}'
```

### Create Transaction (with API Key)

```bash
curl -X POST http://localhost:8000/transactions/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{"amount": 5000, "category_id": 1, "type": "expense", "description": "Coffee"}'
```

## Testing

```bash
# Run tests inside the container
docker-compose exec app pytest
```

## Environment Variables


| Variable | Description | Default |
|------------|----------|--------------|
| DATABASE_URL | PostgreSQL connection URL | postgresql+asyncpg://postgres:mysecretpassword@db:5432/finance_db |
| SECRET_KEY | Secret key for JWT | super-secret-key |
| ALGORITHM | JWT algorithm | HS256 |
| API_KEY | Access key for the API | super-secret-key |

## Migrations

```bash
# Create a new migration
docker-compose exec app alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec app alembic upgrade head
```