import logging

from fastapi import FastAPI

from models.base import Base
from models.product import (
    Product,  # Важливо імпортувати, щоб SQLAlchemy побачила модель
)
from routers.files import router as files_router  # <-- ДОДАНО імпорт роутера файлів

# 1. Імпортуємо створені роутери
from routers.products import router as products_router

# Імпортуємо інструменти бази даних
from settings.db import engine

# 2. Налаштовуємо базове виведення логів
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Змінюємо опис на Практичну роботу №7
app = FastAPI(title="Product Management API", description="Практична робота №7")

# 3. Підключаємо роутери до головного додатка
app.include_router(products_router)
app.include_router(files_router)  # <-- ДОДАНО підключення роутера файлів


@app.get("/")
async def root():
    return {"status": "API is working"}
