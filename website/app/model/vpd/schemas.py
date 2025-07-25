from pydantic import BaseModel
from datetime import date

class VPDSchema(BaseModel):
    military_rank: str
    full_name: str
    departure_date: date
    where_to: str
    arrival_date: date
    military_unit: str
    service_base: str
    current_time: date

    class Config:
        from_attributes = True  # Включение режима работы с SQLAlchemy объектами
