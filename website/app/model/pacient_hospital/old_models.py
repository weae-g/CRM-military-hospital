from ..database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, Boolean, Date

class PatientData(Base):
    __tablename__ = 'patient_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    history_number = Column(Text)
    military_rank = Column(Text)
    service_basis = Column(Text)
    military_unit = Column(Text)
    military_commissariat = Column(Text)
    district = Column(Text)
    full_name = Column(Text)
    birthday_date = Column(Date)
    address = Column(Text)
    phone_number = Column(Text)
    personal_data = Column(Text)
    availability = Column(Text)
    assigned_by = Column(Text)
    admission_date = Column(Date)
    illness_date = Column(Date)
    diagnosis = Column(Text)
    department = Column(Text)
    nature_of_hospitalization = Column(Text)
    transfer = Column(Text)
    departure = Column(Date)