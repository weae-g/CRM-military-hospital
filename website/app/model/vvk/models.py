from sqlalchemy import Column, Integer, Text, Date
from ..database.database import Base

class VVK(Base):
    """
    Модель SQLAlchemy для таблицы 'vvk'.
    
    Атрибуты:
        id (int): Уникальный идентификатор записи, первичный ключ.
        content (str): Содержание записи.
        number (str): Номер записи.
        date_vvk (date): Дата записи.
        full_name (str): Полное имя.
        birthday (date): Дата рождения.
        military_unit (str): Воинская часть.
        military_rank (str): Воинское звание.
        currnt_time (date): Дата создания.
    """
    __tablename__ = 'vvk'
    
    id = Column(Integer, primary_key=True, nullable=False)  # Уникальный идентификатор записи
    content = Column(Text)  # Содержание записи
    number = Column(Text)  # Номер записи
    date_vvk = Column(Date)  # Дата записи
    full_name = Column(Text)  # Полное имя
    birthday = Column(Date)  # Дата рождения
    military_unit = Column(Text)  # Воинская часть
    military_rank = Column(Text)  # Воинское звание
    current_time = Column(Date) # Дата создания
