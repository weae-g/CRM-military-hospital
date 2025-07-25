from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    """
    Схема данных для создания нового документа.
    
    Атрибуты:
        title (str): Заголовок документа.
        description (Optional[str]): Описание документа (необязательный).
        file_path (str): Путь к файлу документа.
    """
    title: str
    description: Optional[str] = None
    file_path: str

class Document(BaseModel):
    """
    Схема данных для представления документа.
    
    Атрибуты:
        id (int): Уникальный идентификатор документа.
        title (str): Заголовок документа.
        description (Optional[str]): Описание документа (необязательный).
        file_path (str): Путь к файлу документа.
        created_at (datetime): Дата и время создания записи.
    """
    id: int
    title: str
    description: Optional[str] = None
    file_path: str
    created_at: datetime

    class Config:
        """
        Конфигурация Pydantic для работы с ORM.
        Включает поддержку преобразования данных из ORM-моделей.
        """
        orm_mode = True
