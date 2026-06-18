from fastapi import FastAPI, HTTPException, status

from settings.db import ping

# Ініціалізуємо додаток FastAPI
app = FastAPI(
    title="FastAPI Docker App",
    description="Практична робота №2: Контейнеризація та асинхронна PostgreSQL",
)


# Базовий ендпойнт, який ви створили у першій практичній
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Новий ендпойнт для перевірки зв'язку з базою даних
@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def db_healthcheck():
    is_alive = await ping()  # Викликаємо функцію ping з файлу settings/db.py
    if not is_alive:
        # Якщо база не відповідає, повертаємо помилку 503 (Сервіс недоступний)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
    # Якщо все добре, повертаємо успішний статус
    return {"status": "healthy", "database": "connected"}
