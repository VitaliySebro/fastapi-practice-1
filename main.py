import logging

from fastapi import FastAPI

from models.base import Base
from models.product import (
    Product,  # Важливо імпортувати, щоб SQLAlchemy побачила модель
)
from models.user import User  # <-- ДОДАНО імпорт моделі користувача для SQLAlchemy
from routers.auth import router as auth_router  # <-- ДОДАНО імпорт роутера авторизації

# 1. Імпортуємо створені роутери
from routers.files import router as files_router
from routers.products import router as products_router

# Імпортуємо інструменти бази даних
from settings.db import engine

# 2. Налаштовуємо базове виведення логів
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Змінюємо опис на Практичну роботу №8
app = FastAPI(
    title="Product Management API", description="Практична робота №8 (JWT & RBAC)"
)

# 3. Підключаємо роутери до головного додатка
app.include_router(auth_router)  # <-- ДОДАНО підключення роутера авторизації
app.include_router(products_router)
app.include_router(files_router)


@app.get("/")
async def root():
    return {"status": "API is working"}
