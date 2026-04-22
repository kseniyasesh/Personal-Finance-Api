# 💰 Personal Finance API

REST API для учета личных финансов на FastAPI с PostgreSQL.

> Проект реализован в рамках практического трека на платформе [Solvit](https://solvit.space/projects/personal_finance_tracker)

## Стек технологий

- Python 3.12
- FastAPI
- PostgreSQL 15
- SQLAlchemy 2.0 (async)
- Alembic
- Pydantic V2
- JWT аутентификация
- Docker & Nginx

## Структура проекта

```
app/
├── main.py           # Точка входа и конфигурация
├── database.py       # Подключение к БД и сессии
├── models.py         # SQLAlchemy модели
├── schemas.py        # Pydantic схемы
├── security.py       # JWT, хеширование и токены
└── routers/          # Роутеры по модулям
    ├── categories.py # Категории
    ├── transactions.py # Транзакции (ACID, Фильтры)
    └── reports.py    # Аналитика и отчеты
migrations/           # История миграций базы данных
tests/                # Автоматические тесты (Pytest)
```

## Быстрый старт

### С Docker (рекомендуется)

```bash
# Клонировать репозиторий
git clone https://github.com
cd Personal-Finance-Api

# Создать .env файл
cp .env.example .env

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

### Аутентификация


| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | /auth/login | Вход (получение Access и Refresh токенов) |

### Транзакции


| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | /transactions/ | Список операций (пагинация, фильтры) | Все |
| POST | /transactions/ | Добавить операцию (защита ACID) | Все |
| GET | /transactions/report | Быстрый отчет по категориям | Все |

### Аналитика (Reports)


| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /reports/categories | Суммарные траты по категориям |
| GET | /reports/timeseries | Динамика расходов по дням |
| GET | /reports/budgets/progress | Состояние лимитов бюджетов |

## Примеры запросов

### Вход

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}'
```

### Создание транзакции (с API Key)

```bash
curl -X POST http://localhost:8000/transactions/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{"amount": 5000, "category_id": 1, "type": "expense", "description": "Coffee"}'
```

## Тестирование

```bash
# Запустить тесты внутри контейнера
docker-compose exec app pytest
```

## Переменные окружения


| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| DATABASE_URL | URL подключения к PostgreSQL | postgresql+asyncpg://postgres:mysecretpassword@db:5432/finance_db |
| SECRET_KEY | Секретный ключ для JWT | super-secret-key |
| ALGORITHM | Алгоритм JWT | HS256 |
| API_KEY | Ключ доступа для API | super-secret-key |

## Миграции

```bash
# Создать новую миграцию
docker-compose exec app alembic revision --autogenerate -m "description"

# Применить миграции
docker-compose exec app alembic upgrade head
```
