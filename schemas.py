from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

# --- Схемы для КАТЕГОРИЙ ---
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Схемы для ТРАНЗАКЦИЙ ---
class TransactionBase(BaseModel):
    amount: int = Field(..., gt=0) # Сумма должна быть больше 0 (gt = greater than)
    description: str | None = Field(default=None, max_length=255)
    category_id: int

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Сумма должна быть положительной")
        return v

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    # Вложенная схема: при получении транзакции мы увидим и данные категории
    category: CategoryResponse 

    model_config = ConfigDict(from_attributes=True)

# --- Схемы для ОТЧЕТОВ ---
class CategoryReport(BaseModel):
    category_name: str
    total_amount: int

