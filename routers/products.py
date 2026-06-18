# routers/products.py
import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product
from schemas.product import ProductCreate, ProductRead, ProductUpdate

# Імпорти з твого проєкту
from settings.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


# 1. Отримання списку всіх товарів (READ - GET)
@router.get("/", response_model=List[ProductRead])
async def get_products(db: SessionDepend):
    try:
        result = await db.execute(select(Product))
        products = result.scalars().all()
        return products
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Помилка отримання списку товарів: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутрішня помилка сервера при отриманні списку товарів.",
        )


# 2. Отримання одного товару за ID (READ - GET)
@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: SessionDepend):
    try:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар з ID {product_id} не знайдено.",
            )
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Помилка отримання товару {product_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутрішня помилка сервера.",
        )


# 3. Створення нового товару (CREATE - POST)
@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: SessionDepend):
    try:
        new_product = Product(**product_in.model_dump())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Помилка створення товару: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не вдалося створити товар.",
        )


# 4. Оновлення існуючого товару (UPDATE - PATCH)
@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, product_in: ProductUpdate, db: SessionDepend):
    try:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар з ID {product_id} не знайдено для оновлення.",
            )

        update_data = product_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)

        await db.commit()
        await db.refresh(product)
        return product
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Помилка оновлення товару {product_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутрішня помилка сервера при оновленні.",
        )


# 5. Видалення товару (DELETE)
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: SessionDepend):
    try:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар з ID {product_id} не знайдено для видалення.",
            )

        await db.delete(product)
        await db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Помилка видалення товару {product_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутрішня помилка сервера при видаленні.",
        )
