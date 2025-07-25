from sqlalchemy import Column, Integer, Text
from ..database.database import Base
from datetime import datetime

class DocumentDB(Base):
    """
    Модель SQLAlchemy для таблицы 'documents'.
    
    Атрибуты:
        id (int): Уникальный идентификатор документа, первичный ключ.
        title (str): Заголовок документа.
        description (str): Описание документа.
        file_path (str): Путь к файлу документа.
        created_at (datetime): Дата и время создания записи (по умолчанию текущее время).
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, index=True)  # Заголовок документа
    description = Column(Text, index=True)  # Описание документа
    file_path = Column(Text, index=True)  # Путь к файлу документа
    created_at = Column(Text, default=datetime.utcnow)  # Дата и время создания записи
