from sqlalchemy import Column, Integer, Text
from ..database.database import Base

class UserDB(Base):
    """
    Модель SQLAlchemy для таблицы 'users'.
    
    Атрибуты:
        id (int): Уникальный идентификатор пользователя, первичный ключ.
        username (str): Имя пользователя.
        password (str): Пароль пользователя.
        ip_addresses (str): IP-адреса пользователя.
        full_name (str): Полное имя пользователя.
        cabinet (str): Кабинет пользователя.
        role (str): Роль пользователя.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор
    username = Column(Text, nullable=False, index=True)  # Имя пользователя
    password = Column(Text, nullable=False)  # Пароль пользователя
    ip_addresses = Column(Text)  # IP-адреса пользователя
    full_name = Column(Text, nullable=False)  # Полное имя пользователя
    cabinet = Column(Text)  # Кабинет пользователя
    role = Column(Text, nullable=False)  # Роль пользователя

    # Обратите внимание, что для полей, таких как `created_at`, можно добавить `default` значения
    # В этом примере `created_at` не включен, но если вам нужно его добавить, вы можете сделать это следующим образом:
    # created_at = Column(DateTime, default=datetime.utcnow)  # Дата и время создания записи
