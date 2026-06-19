# utils/dependencies.py
from authx import RequestToken
from fastapi import Depends, HTTPException, status

from models.user import UserRole
from utils.security import security


# 1. Базова залежність: просто вимагає наявність БУДЬ-ЯКОГО валідного токена.
# Якщо токена немає або він прострочений — AuthX автоматично викине помилку 401.
def get_current_token(
    token: RequestToken = Depends(security.access_token_required),
) -> RequestToken:
    return token


# 2. Фабрика залежностей для перевірки конкретних ролей (RBAC).
class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, token: RequestToken = Depends(get_current_token)):
        # Дістаємо роль користувача з payload токена, яку ми зберегли при авторизації
        user_role = token.payload.get("role")

        # Перевіряємо, чи є роль користувача серед дозволених
        if user_role not in [role.value for role in self.allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас недостатньо прав для виконання цієї дії.",
            )
        return token
