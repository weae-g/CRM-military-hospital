from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ..database.database import Base
from datetime import datetime
from pytz import timezone

# Устанавливаем временную зону Москвы
moscow_tz = timezone('Europe/Moscow')

# Функция для получения текущего времени в Москве
def get_moscow_time():
    return datetime.now(moscow_tz)

class ClinicData(Base):
    """
    Модель SQLAlchemy для таблицы 'clinic_data'.
    
    Атрибуты:
        id (int): Уникальный идентификатор записи, первичный ключ.
        full_name (str): Полное имя пациента.
        directed (str): Направление.
        birthday (datetime): Дата рождения.
        address (str): Адрес.
        policy_CMI (str): Полис ОМС.
        snils (str): СНИЛС.
        document (str): Документ.
        military_unit (str): Воинская часть.
        military_rank (str): Воинское звание.
        belonging (str): Принадлежность.
        hostilities (bool): Участие в боевых действиях.
        personal_number (str): Личный номер.
        military_commissariat (str): Военный комиссариат.
        military_district (str): Военный округ.
        phone_number (str): Номер телефона.
        card_number (str): Номер карты.
        patient_info (str): Информация о пациенте.
        medical_type (str): Тип медицинской помощи.
        current_time (datetime): Текущее время в Москве.
        vkk_info (str): Информация о ВВК. (не будет)
        hospitalization_info (str): Информация о госпитализации. (не будет)
    """
    __tablename__ = 'clinic_data'
    
    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(Text, nullable=False, index=True)  # Полное имя пациента
    directed  = Column(Text)  # Направление
    birthday = Column(DateTime)  # Дата рождения
    address = Column(Text)  # Адрес
    policy_CMI = Column(Text)  # Полис ОМС
    snils = Column(Text)  # СНИЛС
    document = Column(Text)  # Документ
    military_unit = Column(Text)  # Воинская часть
    military_rank = Column(Text)  # Воинское звание
    belonging = Column(Text)  # Принадлежность
    hostilities = Column(Boolean)  # Участие в боевых действиях
    personal_number = Column(Text)  # Личный номер
    military_commissariat = Column(Text)  # Военный комиссариат
    military_district = Column(Text)  # Военный округ
    phone_number = Column(Text)  # Номер телефона
    card_number = Column(Text, index=True)  # Номер карты
    patient_info = Column(Text)  # Информация о пациенте
    medical_type = Column(Text)  # Тип медицинской помощи
    current_time = Column(DateTime, nullable=False, default=get_moscow_time)  # Текущее время в Москве
    vkk_info = Column(Text)  # Информация о ВВК
    hospitalization_info = Column(Text)  # Информация о госпитализации

    # Связи с другими таблицами
    appointments = relationship("ClinicAppointment", back_populates="patient")
    hospitalizations = relationship("HospitalizationClinic", back_populates="patient")
    vvks = relationship("VvkClinic", back_populates="patient")

class DoctorsOfTheClinic(Base):
    """
    Модель SQLAlchemy для таблицы 'doctors_of_the_clinic'.
    
    Атрибуты:
        id (int): Уникальный идентификатор записи, первичный ключ.
        doctor_type (str): Тип врача.
        full_name (str): Полное имя врача.
        cabinet (str): Кабинет врача.
        phone_number (str): Номер телефона врача.
    """
    __tablename__ = 'doctors_of_the_clinic'
    
    id = Column(Integer, primary_key=True, nullable=False)
    doctor_type = Column(Text, nullable=False)  # Тип врача
    full_name = Column(Text, nullable=False)  # Полное имя врача
    cabinet = Column(Text)  # Кабинет врача
    phone_number = Column(Text)  # Номер телефона врача

    # Связь с таблицей назначений
    hospital_record_apply = relationship("HospitalRecord", back_populates="doctor")
    appointments = relationship("ClinicAppointment", back_populates="doctor")

class ClinicAppointment(Base):
    """
    Модель SQLAlchemy для таблицы 'clinic_appointment'.
    
    Атрибуты:
        id (int): Уникальный идентификатор записи, первичный ключ.
        patient_id (int): Внешний ключ на пациента.
        doctor_id (int): Внешний ключ на врача.
        datetime_q (datetime): Дата и время назначения.
        note (str): Примечание.
        doctor_report (str): Отчёт врача.
        doctor_note (str): Заметка врача.
    """
    __tablename__ = 'clinic_appointment'
        
    id = Column(Integer, primary_key=True, nullable=False)
    patient_id = Column(Integer, ForeignKey('clinic_data.id'), nullable=False)  # Внешний ключ на пациента
    doctor_id = Column(Integer, ForeignKey('doctors_of_the_clinic.id'), nullable=False)  # Внешний ключ на врача
    datetime_q = Column(DateTime)  # Дата и время назначения
    note = Column(Text)  # Примечание
    doctor_report = Column(Text)  # Отчёт врача
    doctor_note = Column(Text)  # Заметка врача

    # Связи с таблицами пациентов и врачей
    patient = relationship("ClinicData", back_populates="appointments")
    doctor = relationship("DoctorsOfTheClinic", back_populates="appointments")

class HospitalizationClinic(Base):
    """
    Модель SQLAlchemy для таблицы 'hospitalization_clinic'.
    
    Атрибуты:
        id (int): Уникальный идентификатор записи, первичный ключ.
        patient_id (int): Внешний ключ на пациента.
        date (date): Дата госпитализации.
        diagnosis (str): Диагноз.
        direction (str): Направление.
    """
    __tablename__ = 'hospitalization_clinic'

    id = Column(Integer, primary_key=True, nullable=False)
    patient_id = Column(Integer, ForeignKey('clinic_data.id'), nullable=False)  # Внешний ключ на пациента
    date = Column(Date)  # Дата госпитализации
    diagnosis = Column(Text)  # Диагноз
    direction = Column(Text)  # Направление

    # Связь с таблицей пациентов
    patient = relationship("ClinicData", back_populates="hospitalizations")

class VvkClinic(Base):
    """
    Модель SQLAlchemy для таблицы 'vvk_clinic'.
    
    Атрибуты:
        id (int): Уникальный идентификатор записи, первичный ключ.
        patient_id (int): Внешний ключ на пациента.
        vvk_date (date): Дата ВВК.
        vvk_number (str): Номер ВВК.
        conclusion (str): Заключение ВВК.
    """
    __tablename__ = 'vvk_clinic'

    id = Column(Integer, primary_key=True, nullable=False)
    patient_id = Column(Integer, ForeignKey('clinic_data.id'), nullable=False)  # Внешний ключ на пациента
    vvk_date = Column(Date, nullable=False)  # Дата ВВК
    vvk_number = Column(Text, nullable=False)  # Номер ВВК
    conclusion = Column(Text, nullable=False)  # Заключение ВВК

    # Связь с таблицей пациентов
    patient = relationship("ClinicData", back_populates="vvks")
