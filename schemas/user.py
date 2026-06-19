# schemas/user.py
from pydantic import BaseModel, EmailStr

from models.user import UserRole


# Схема для реєстрації: клієнт обов'язково передає всі три поля
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# Схема для відповіді: повертаємо інформацію про користувача безпечно (без пароля)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    role: UserRole

    class Config:
        from_attributes = (
            True  # Дозволяє Pydantic працювати з об'єктами SQLAlchemy (ORM)
        )


# Схема для повернення токена після успішної авторизації
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
