# utils/security.py
from authx import AuthX, AuthXConfig
from passlib.context import CryptContext

# Конфігурація налаштувань для AuthX
config = AuthXConfig()
config.JWT_SECRET_KEY = "your-super-secret-key"  # Секретний ключ для шифрування JWT
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["headers"]

# Ініціалізація об'єкта системи безпеки
security = AuthX(config=config)

# Налаштування контексту для безпечного хешування паролів за алгоритмом bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функція для перевірки, чи збігається введений пароль із хешем з бази даних
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Функція для створення безпечного хешу з чистого пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
