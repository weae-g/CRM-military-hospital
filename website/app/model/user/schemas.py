from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    """
    Схема данных для создания нового пользователя.

    Атрибуты:
        username (str): Имя пользователя.
        password (str): Пароль пользователя.
        ip_addresses (Optional[str]): IP-адреса пользователя (необязательный).
        full_name (str): Полное имя пользователя.
        cabinet (Optional[str]): Кабинет пользователя (необязательный).
        role (str): Роль пользователя.
    """
    username: str
    password: str
    ip_addresses: Optional[str] = None
    full_name: str
    cabinet: Optional[str] = None
    role: str

class User(BaseModel):
    """
    Схема данных для представления пользователя.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        username (str): Имя пользователя.
        password (str): Пароль пользователя.
        ip_addresses (Optional[str]): IP-адреса пользователя (необязательный).
        full_name (str): Полное имя пользователя.
        cabinet (Optional[str]): Кабинет пользователя (необязательный).
        role (str): Роль пользователя.
    """
    id: int
    username: str
    password: str
    ip_addresses: Optional[str] = None
    full_name: str
    cabinet: Optional[str] = None
    role: str

    class Config:
        """
        Конфигурация Pydantic для работы с ORM.
        Включает поддержку преобразования данных из ORM-моделей.
        """
        orm_mode = True
