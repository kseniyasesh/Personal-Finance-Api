from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import categories
from app.database import engine, Base
from app.routers import transactions
from app.routers import reports
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

API_KEY = "super-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Personal Finance API",
    version="0.2.0",
    lifespan=lifespan
)

# ПОДКЛЮЧАЕМ РОУТЕРЫ
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return {"message": "Finance API is working", "docs": "/docs"}
