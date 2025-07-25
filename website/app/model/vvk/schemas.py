from pydantic import BaseModel
from typing import Optional
from datetime import date

class VVKBase(BaseModel):
    """
    Базовая модель Pydantic для сущности ВВК.

    Атрибуты:
        content (str): Содержание записи.
        number (str): Номер записи.
        date_vvk (date): Дата записи.
        full_name (str): Полное имя.
        birthday (date): Дата рождения.
        military_unit (Optional[str]): Воинская часть (необязательно).
        military_rank (Optional[str]): Воинское звание (необязательно).
    """
    content: str  # Содержание записи
    number: str  # Номер записи
    date_vvk: date  # Дата записи
    full_name: str  # Полное имя
    birthday: date  # Дата рождения
    military_unit: Optional[str] = None  # Воинская часть (необязательно)
    military_rank: Optional[str] = None  # Воинское звание (необязательно)

class VVKCreate(VVKBase):
    """
    Модель Pydantic для создания новой записи ВВК.
    Наследуется от VVKBase.
    """
    pass

class VVKUpdate(VVKBase):
    """
    Модель Pydantic для обновления существующей записи ВВК.
    Наследуется от VVKBase.
    """
    pass

class VVK(VVKBase):
    """
    Модель Pydantic для отображения записи ВВК.
    Наследуется от VVKBase и добавляет идентификатор записи.
    
    Атрибуты:
        id (int): Уникальный идентификатор записи.
    """
    id: int  # Уникальный идентификатор записи

    class Config:
        orm_mode = True  # Включение режима ORM для поддержки SQLAlchemy моделей
