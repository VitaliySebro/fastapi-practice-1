# main.py
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from models.base import Base
from models.product import (
    Product,  # Важливо імпортувати, щоб SQLAlchemy побачила модель
)

# 1. Імпортуємо створений роутер
from routers.products import router as products_router

# Імпортуємо інструменти бази даних
from settings.db import engine

# # 2. Налаштовуємо базове виведення логів (змінюємо INFO на WARNING, щоб не було спаму)
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Функція, яка автоматично створить таблицю products при старті сервера
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.warning("Автоматичне створення таблиць бази даних...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Product Management API", description="Практична робота №5", lifespan=lifespan
)

# # 3. Підключаємо роутер товарів до головного додатка (Обов'язково додаємо цей рядок!)
app.include_router(products_router)


@app.get("/")
async def root():
    return {"status": "API is working"}
