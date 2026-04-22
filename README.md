# 💰 Personal Finance API

REST API для учета личных финансов на FastAPI с PostgreSQL.

> Проект реализован в рамках практического трека на платформе [Solvit](https://solvit.space/projects/personal_finance_tracker).

## Стек технологий

- Python 3.12
- FastAPI (Async)
- PostgreSQL 15
- SQLAlchemy 2.0 (Async)
- Alembic (Миграции)
- Pydantic V2
- Docker & Docker Compose
- API Key Security (Middleware)

## Структура проекта

```
app/
├── main.py           # Точка входа и конфигурация API
├── database.py       # Подключение к БД и управление сессиями
├── models.py         # SQLAlchemy модели (структура таблиц)
├── schemas.py        # Pydantic схемы (валидация запросов)
└── routers/          # Модульные эндпоинты
    ├── categories.py # Управление категориями
    ├── transactions.py # Доходы и расходы (CRUD)
    └── reports.py    # Аналитика (Категории, Динамика, Бюджеты)
migrations/           # История миграций базы данных
tests/                # Автоматические тесты (Pytest)
```

## Быстрый старт

### С Docker (рекомендуется)

```bash
# Клонировать репозиторий
git clone https://github.com
cd Personal-Finance-Api

# Запустить контейнеры
docker-compose up --build -d

# Применить миграции
docker-compose exec app alembic upgrade head
```

API будет доступен по адресу: http://localhost:8000
Swagger UI: http://localhost:8000/docs

### Локально (без Docker)

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload
```

## API Endpoints

### Categories


| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | /categories/ | Создать новую категорию |

### Transactions


| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /transactions/ | Список операций (фильтры: дата, категория, тип) |
| POST | /transactions/ | Добавить новую операцию |
| GET | /transactions/report | Агрегированный отчет по категориям |

### Reports (Аналитика Solvit)


| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /reports/categories | Суммарный отчет по категориям за период |
| GET | /reports/timeseries | Динамика расходов по дням |
| GET | /reports/budgets/progress | Прогресс по бюджетам (Лимит/Остаток) |

### System


| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | / | Проверка статуса API (Root) |

## Примеры запросов (CURL)

### Добавление транзакции
```bash
curl -X POST http://localhost:8000/transactions/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{"amount": 5000, "category_id": 1, "description": "Кофе", "type": "expense", "date": "2024-04-22"}'
```

## Тестирование

```bash
# Запуск тестов внутри контейнера
docker-compose exec app pytest tests/test_main.py
```

## Миграции

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "описание"

# Применить миграции
alembic upgrade head
```