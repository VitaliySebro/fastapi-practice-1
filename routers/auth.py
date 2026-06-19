# routers/auth.py
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Імпорти відповідно до структури твого проєкту
from models.user import User, UserRole
from schemas.user import TokenResponse, UserCreate, UserResponse
from settings.db import get_db
from utils.security import get_password_hash, security, verify_password

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Authentication"])


# 1. Ендпойнт для реєстрації нового користувача
@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Перевіряємо, чи немає вже користувача з таким email або username
    result = await db.execute(
        select(User).where(
            (User.email == user_in.email) | (User.username == user_in.username)
        )
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Користувач з таким email або username вже існує.",
        )

    # Хешуємо пароль перед збереженням в базу
    hashed_pwd = get_password_hash(user_in.password)

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_pwd,
        role=UserRole.USER,  # За замовчуванням всі нові користувачі мають роль USER
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# 2. Ендпойнт логіну за стандартом OAuth2 (Генерація JWT-токена)
@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # Форма OAuth2PasswordRequestForm приймає пошту/логін у поле credentials.username
    result = await db.execute(select(User).where(User.email == credentials.username))
    user = result.scalar_one_or_none()

    # Перевіряємо, чи існує користувач і чи збігається хеш пароля
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний email або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Користувач неактивний або заблокований",
        )

    # Генеруємо токен і зашиваємо туди роль та email для перевірки прав (RBAC)
    access_token = security.create_access_token(
        uid=str(user.id), data={"role": user.role.value, "email": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}
