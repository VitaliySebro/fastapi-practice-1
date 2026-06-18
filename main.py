from contextlib import asynccontextmanager

from fastapi import FastAPI

# Імпортуємо Base. Через нього SQLAlchemy побачить усі моделі, які ми щойно зареєстрували
from models import Base

# Імпортуємо ваш асинхронний двигун бази даних
from settings.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код у цьому блоці виконується ОДИН РАЗ при СТАРТІ додатка
    async with engine.begin() as conn:
        # Автоматично створюємо всі таблиці в базі даних (User, Profile, Chat тощо)
        await conn.run_sync(Base.metadata.create_all)
        print("🎉 Базу даних успішно синхронізовано! Таблиці месенджера створено.")

    yield  # Тут додаток запускається і чекає на запити користувачів

    # Код тут виконується при ЗУПИНЦІ додатка
    await engine.dispose()
    print("💤 З'єднання з базою даних закрито.")


# Створюємо додаток FastAPI та передаємо йому налаштований lifespan
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "FastAPI працює, таблиці успішно згенеровано!",
    }
