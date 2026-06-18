from typing import Optional

from pydantic import BaseModel, Field


# 1. Базова схема з спільними полями для всіх операцій
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Назва товару")
    description: Optional[str] = Field(None, description="Опис товару")
    price: float = Field(..., gt=0, description="Ціна повинна бути більшою за 0")
    quantity: int = Field(..., ge=0, description="Кількість не може бути від'ємною")


# 2. Схема для створення (CREATE) — наслідує всі базові поля
class ProductCreate(ProductBase):
    pass


# 3. Схема для оновлення (UPDATE) — робимо всі поля Optional,
# щоб можна було оновити лише одне конкретне поле через PATCH
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)


# 4. Схема для відповіді клієнту (READ) — додає id, яке генерує БД
class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = (
            True  # Дозволяє Pydantic працювати з моделями SQLAlchemy (як ORM)
        )
