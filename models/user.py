import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# 1. Додаємо Enum для ролей користувачів
class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 2. Додаємо нові обов'язкові колонки з server_default
    is_active: Mapped[bool] = mapped_column(
        nullable=False, server_default=text("true"), default=True
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
        server_default=text("'user'"),
        default=UserRole.USER,
    )

    # Існуючі зв'язки залишаються без змін
    profile: Mapped["Profile"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    chats: Mapped[list["ChatMember"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="sender", cascade="all, delete-orphan"
    )
