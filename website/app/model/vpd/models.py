from sqlalchemy import Column, Integer, String, Date
from ..database.database import Base


class VPD(Base):
    __tablename__ = 'vpd'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    military_rank = Column(String)
    full_name = Column(String)
    departure_date = Column(Date)
    where_to = Column(String)
    arrival_date = Column(Date)
    military_unit = Column(String)
    service_base = Column(String)
    current_time = Column(Date)
