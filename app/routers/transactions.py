from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
import app.models as models, app.schemas as schemas
from typing import Optional
from fastapi import BackgroundTasks

router = APIRouter(prefix="/transactions", tags=["Transactions"])

def send_transaction_notification(amount: int):
    print(f"Фоновая задача: Обработка транзакции на сумму {amount} копеек завершена.")

@router.post("/", response_model=schemas.TransactionResponse)
async def create_transaction(
    transaction: schemas.TransactionCreate, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Category).where(models.Category.id == transaction.category_id).with_for_update()  
    result = await db.execute(query)
    category = result.scalars().first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")     
    
    new_transaction = models.Transaction(**transaction.model_dump())
    db.add(new_transaction)
    background_tasks.add_task(send_transaction_notification, transaction.amount) 
    return new_transaction



@router.get("/", response_model=list[schemas.TransactionResponse])
async def get_transactions(
    limit: int = 10,        # Сколько штук показать
    offset: int = 0,       # Сколько пропустить (для страниц)
    min_amount: Optional[int] = None, # Фильтр "ОТ"
    max_amount: Optional[int] = None, # Фильтр "ДО"
    db: AsyncSession = Depends(get_db)
):
    # Создаем базовый запрос
    query = select(models.Transaction)
    
    # Динамически добавляем фильтры по суммам (если они переданы)
    if min_amount is not None:
        query = query.where(models.Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.where(models.Transaction.amount <= max_amount)
    
    # Применяем пагинацию (limit и offset)
    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    return result.scalars().all()



@router.get("/report", response_model=list[schemas.CategoryReport])
async def get_category_report(db: AsyncSession = Depends(get_db)):
    query = (
        select(models.Category.name, func.sum(models.Transaction.amount).label("total_amount"))
        .join(models.Transaction).group_by(models.Category.name)
    )
    result = await db.execute(query)
    return [{"category_name": row[0], "total_amount": row[1]} for row in result.all()]
