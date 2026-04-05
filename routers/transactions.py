from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
import models, schemas

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=schemas.TransactionResponse)
async def create_transaction(transaction: schemas.TransactionCreate, db: AsyncSession = Depends(get_db)):
    category_check = await db.execute(select(models.Category).where(models.Category.id == transaction.category_id))
    if not category_check.scalars().first():
        raise HTTPException(status_code=404, detail="Category not found")
    new_transaction = models.Transaction(**transaction.model_dump())
    db.add(new_transaction)
    await db.flush()
    await db.refresh(new_transaction)
    return new_transaction

@router.get("/", response_model=list[schemas.TransactionResponse])
async def get_transactions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Transaction))
    return result.scalars().all()

@router.get("/report", response_model=list[schemas.CategoryReport])
async def get_category_report(db: AsyncSession = Depends(get_db)):
    query = (
        select(models.Category.name, func.sum(models.Transaction.amount).label("total_amount"))
        .join(models.Transaction).group_by(models.Category.name)
    )
    result = await db.execute(query)
    return [{"category_name": row[0], "total_amount": row[1]} for row in result.all()]
