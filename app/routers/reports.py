from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Transaction, Budget
from datetime import date

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/categories")
async def get_categories_report(from_date: date, to_date: date, session: AsyncSession = Depends(get_db)):
    # Считаем суммы по категориям
    query = (
        select(Transaction.category_id, func.sum(Transaction.amount).label("total"))
        .where(Transaction.date.between(from_date, to_date))
        .group_by(Transaction.category_id)
    )
    result = await session.execute(query)
    # Обращаемся по именам полей .category_id и .total — это надежнее индексов
    return [{"category_id": r.category_id, "total": r.total} for r in result.all()]

@router.get("/timeseries")
async def get_timeseries_report(from_date: date, to_date: date, session: AsyncSession = Depends(get_db)):
    # Динамика трат по дням
    query = (
        select(Transaction.date, func.sum(Transaction.amount).label("day_total"))
        .where(Transaction.date.between(from_date, to_date))
        .group_by(Transaction.date)
        .order_by(Transaction.date)
    )
    result = await session.execute(query)
    return [{"date": r.date, "total": r.day_total} for r in result.all()]

@router.get("/budgets/progress")
async def get_budget_progress(session: AsyncSession = Depends(get_db)):
    # Прогресс бюджетов: Лимит vs Потрачено
    spent_query = (
        select(Transaction.category_id, func.sum(Transaction.amount).label("spent"))
        .group_by(Transaction.category_id)
    )
    spent_res = await session.execute(spent_query)
    spent_dict = {row.category_id: row.spent for row in spent_res.all()}

    budget_res = await session.execute(select(Budget))
    budgets = budget_res.scalars().all()

    return [
        {
            "category_id": b.category_id,
            "limit": b.amount,
            "spent": spent_dict.get(b.category_id, 0),
            "remaining": b.amount - spent_dict.get(b.category_id, 0)
        } for b in budgets
    ]
