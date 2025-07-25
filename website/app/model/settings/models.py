from sqlalchemy import Column, Integer, Text
from ..database.database import Base

class Document(Base):
    """
    Модель SQLAlchemy для таблицы 'documents_aut'.
    
    Атрибуты:
        id (int): Уникальный идентификатор документа, первичный ключ.
        branch (str): Отдел или филиал, к которому относится документ.
        name (str): Имя документа.
        job_title (str): Должность, связанная с документом.
        rank (str): Ранг или статус, связанный с документом.
        places (int): Количество мест или позиций, связанных с документом.
    """
    __tablename__ = "documents_aut"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор документа
    branch = Column(Text, nullable=False)  # Отдел или филиал, к которому относится документ
    name = Column(Text, nullable=False)  # Имя документа
    job_title = Column(Text, nullable=False)  # Должность, связанная с документом
    rank = Column(Text, nullable=False)  # Ранг или статус, связанный с документом
    places = Column(Integer, nullable=False)  # Количество мест или позиций, связанных с документом
