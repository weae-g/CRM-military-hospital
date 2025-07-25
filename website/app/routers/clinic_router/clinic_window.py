# Роутер для управления.

from ...model.сlinic.models import ClinicData as ClinicDataModel

from sqlalchemy.orm import Session
from fastapi import Depends
from ...model.database.database import SessionLocal
from fastapi import HTTPException
from ...model.сlinic.models import ClinicData as ClinicDataModel
from ...model.сlinic.models import DoctorsOfTheClinic, ClinicAppointment, VvkClinic, HospitalizationClinic
from ...model.сlinic.schemas import ClinicData, ClinicDataCreate, ClinicAppointmentCreate, PatientUpdate, VvkCreate, Vvk, HospitalizationCreate, HospitalizationData
from ...model.сlinic.schemas import DoctorsOfTheClinic as DoctorsOfTheClinicSchema
from ...model.сlinic.schemas import ClinicAppointment as ClinicAppointmentSchema
from ...model.сlinic.schemas import UpdatePatientData

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def update_patient_router(patient_id: int, patient_data: UpdatePatientData, db: Session = Depends(get_db)):
    # Поиск пациента в базе данных
    patient = db.query(ClinicDataModel).filter(ClinicDataModel.id == patient_id).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Обновление данных пациента
    for field, value in patient_data.dict(exclude_unset=True).items():
        if hasattr(patient, field):
            setattr(patient, field, value)

    # Сохранение изменений в базе данных
    db.commit()

    return patient

async def create_appointment_router(patient_id: int, appointment_data: dict, db: Session = Depends(get_db)):
    # Создание нового приёма
    appointment = ClinicAppointment(patient_id=patient_id, **appointment_data)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment

async def create_hospitalization_router(patient_id: int, hospitalization_data: dict, db: Session = Depends(get_db)):
    # Создание новой госпитализации
    hospitalization = HospitalizationClinic(patient_id=patient_id, **hospitalization_data)
    db.add(hospitalization)
    db.commit()
    db.refresh(hospitalization)

    return hospitalization

async def create_vvk_router(patient_id: int, vvk_data: dict, db: Session = Depends(get_db)):
    # Создание нового ВВК
    vvk = VvkClinic(patient_id=patient_id, **vvk_data)
    db.add(vvk)
    db.commit()
    db.refresh(vvk)

    return vvk

def delete_appointment_router(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(ClinicAppointment).filter(ClinicAppointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()

    return {"detail": "Appointment deleted"}

def delete_hospitalization_router(hospitalization_id: int, db: Session = Depends(get_db)):
    hospitalization = db.query(HospitalizationClinic).filter(HospitalizationClinic.id == hospitalization_id).first()
    if not hospitalization:
        raise HTTPException(status_code=404, detail="Hospitalization not found")

    db.delete(hospitalization)
    db.commit()

    return {"detail": "Hospitalization deleted"}

async def delete_vvk_router(vvk_id: int, db: Session = Depends(get_db)):
    vvk = db.query(VvkClinic).filter(VvkClinic.id == vvk_id).first()
    if not vvk:
        raise HTTPException(status_code=404, detail="VVK not found")

    db.delete(vvk)
    db.commit()

    return {"detail": "VVK deleted"}
