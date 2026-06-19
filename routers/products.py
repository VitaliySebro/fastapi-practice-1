# routers/products.py
import logging

from authx import RequestToken
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.product import Product  # Твоя модель продукту
from models.user import UserRole
from settings.db import get_db  # Твоя залежність сесії бази даних

# Імпортуємо налаштування захисту, ролі та залежність БД
from utils.dependencies import RoleChecker, get_current_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/products", tags=["Products"])

# Ініціалізуємо перевірку ролі: видалення дозволено ТІЛЬКИ адмінам
admin_only = RoleChecker([UserRole.ADMIN])


# --- МЕТОД 1: Створення товару (Доступно будь-якому авторизованому юзеру) ---
@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create a new product")
async def create_product(
    product_data: dict,  # Заміни dict на свою Pydantic-схему товару (наприклад, ProductCreate)
    db: AsyncSession = Depends(get_db),
    token: RequestToken = Depends(get_current_token),
):
    current_user_id = token.sub  # ID користувача, який робить запит
    logger.info(f"User {current_user_id} is creating a product")

    # Твоя логіка збереження товару в БД. Наприклад:
    # new_product = Product(**product_data.dict())
    # db.add(new_product)
    # await db.commit()

    return {"status": "Product created", "created_by_user_id": current_user_id}


# --- МЕТОД 2: Видалення товару (Доступно ВИКЛЮЧНО Адміністраторам) ---
@router.delete(
    "/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a product"
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    token: RequestToken = Depends(
        admin_only
    ),  # <-- Тут спрацює жорстка перевірка на роль ADMIN
):
    logger.info(f"Admin {token.sub} is attempting to delete product {product_id}")

    # 1. Шукаємо продукт у базі
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не знайдено."
        )

    # 2. Видаляємо продукт
    await db.delete(product)
    await db.commit()

    return None
