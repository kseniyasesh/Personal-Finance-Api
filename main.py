from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from routers import categories, transactions # Импортируем наши новые файлы

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Personal Finance API",
    version="0.2.0",
    lifespan=lifespan
)

# ПОДКЛЮЧАЕМ РОУТЕРЫ
app.include_router(categories.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return {"message": "Finance API is working", "docs": "/docs"}
