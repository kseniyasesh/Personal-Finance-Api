# 💰 Personal Finance Tracker API

Асинхронное REST API для учета личных финансов (доходы, расходы, отчеты) на FastAPI и PostgreSQL.

## 🚀 Стек технологий
* **Python 3.12**
* **FastAPI** (Async)
* **PostgreSQL 15**
* **SQLAlchemy 2.0** (Modern Mapped Style)
* **Pydantic V2** (Validation)
* **Docker & Docker Compose**

## 🏗️ Структура проекта
```
├── main.py           # Точка входа и Lifespan (startup)
├── database.py       # Настройка Async SQLAlchemy & Engine
├── models.py         # SQLAlchemy модели (ORM)
├── schemas.py        # Валидация данных Pydantic
└── routers/          # Разделение логики по модулям
    ├── categories.py
    └── transactions.py
```

## ⚡ Быстрый старт (Docker)
1. Клонируйте репозиторий:
   `git clone https://github.com/kseniyasesh/Personal-Finance-Api.git`
2. Запустите проект одной командой:
   `docker-compose up --build`

API будет доступно по адресу: http://localhost:8000
Swagger UI (Документация): http://localhost:8000/docs

## 📊 Основные эндпоинты

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/categories/` | Создать новую категорию |
| POST | `/transactions/` | Добавить расход/доход |
| GET | `/transactions/` | История всех операций |
| GET | `/transactions/report` | Агрегированный отчет по категориям |

## 🛠️ Особенности реализации
* **Money Handling**: Денежные суммы хранятся в `Integer` (копейки) для исключения ошибок округления `float`.
* **Async Stack**: Полностью асинхронный путь от запроса до базы данных.
* **Relational DB**: Использование `ForeignKeys` и `Relationship` (lazy="joined/selectin") для оптимизации запросов.
