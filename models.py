from datetime import datetime
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    # index=True делает поиск по имени категории мгновенным
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # lazy="selectin" — стандарт для связей "один ко многим"
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category", 
        lazy="selectin"
    )

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column() 
    description: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)
    
    # lazy="joined" подтягивает категорию СРАЗУ в том же запросе (JOIN в SQL)
    category: Mapped["Category"] = relationship(
        back_populates="transactions", 
        lazy="joined"
    )

