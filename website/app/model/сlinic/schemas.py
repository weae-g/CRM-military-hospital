from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class ClinicDataCreate(BaseModel):
    """
    Модель для создания данных о пациенте.

    Атрибуты:
        full_name (str): Полное имя пациента.
        directed (Optional[str]): Направление.
        birthday (Optional[str]): Дата рождения.
        address (Optional[str]): Адрес.
        policy_CMI (Optional[str]): Полис ОМС.
        snils (Optional[str]): СНИЛС.
        document (Optional[str]): Документ.
        military_unit (Optional[str]): Воинская часть.
        military_rank (Optional[str]): Воинское звание.
        belonging (Optional[str]): Принадлежность.
        hostilities (Optional[bool]): Участие в боевых действиях.
        personal_number (Optional[str]): Личный номер.
        military_commissariat (Optional[str]): Военный комиссариат.
        military_district (Optional[str]): Военный округ.
        phone_number (Optional[str]): Номер телефона.
        card_number (Optional[str]): Номер карты.
        patient_info (Optional[str]): Информация о пациенте.
        medical_type (Optional[str]): Тип медицинской помощи.
        current_time (Optional[datetime]): Текущее время.
        vkk_info (Optional[str]): Информация о ВВК.
        hospitalization_info (Optional[str]): Информация о госпитализации.
    """
    full_name: str
    directed: Optional[str] = None
    birthday: Optional[str] = None
    address: Optional[str] = None
    policy_CMI: Optional[str] = None
    snils: Optional[str] = None     
    document: Optional[str] = None
    military_unit: Optional[str] = None
    military_rank: Optional[str] = None
    belonging: Optional[str] = None
    hostilities: Optional[bool] = None
    personal_number: Optional[str] = None
    military_commissariat: Optional[str] = None
    military_district: Optional[str] = None
    phone_number: Optional[str] = None
    card_number: Optional[str] = None
    patient_info: Optional[str] = None
    medical_type: Optional[str] = None
    current_time: Optional[datetime] = None
    vkk_info: Optional[str] = None
    hospitalization_info: Optional[str] = None

class HospitalizationCreate(BaseModel):
    """
    Модель для создания данных о госпитализации.

    Атрибуты:
        patient_id (int): Идентификатор пациента.
        date (date): Дата госпитализации.
        diagnosis (str): Диагноз.
        direction (str): Направление.
    """
    patient_id: int
    date: date
    diagnosis: str
    direction: str

    class Config:
        orm_mode = True

class HospitalizationData(BaseModel):
    """
    Модель данных о госпитализации.

    Атрибуты:
        id (int): Уникальный идентификатор записи.
        patient_id (int): Идентификатор пациента.
        date (date): Дата госпитализации.
        diagnosis (str): Диагноз.
        direction (str): Направление.
    """
    id: int
    patient_id: int
    date: date
    diagnosis: str
    direction: str

    class Config:
        orm_mode = True

class ClinicData(ClinicDataCreate):
    """
    Модель данных о пациенте.

    Атрибуты:
        id (int): Уникальный идентификатор записи.
    """
    id: int

    class Config:
        orm_mode = True

class ClinicAppointmentCreate(BaseModel):
    """
    Модель для создания данных о приеме в клинике.

    Атрибуты:
        patient_id (int): Идентификатор пациента.
        doctor_id (int): Идентификатор врача.
        datetime_q (datetime): Дата и время приема.
        note (Optional[str]): Примечание.
        doctor_report (Optional[str]): Отчет врача.
        doctor_note (Optional[str]): Заметка врача.
    """
    patient_id: int
    doctor_id: int
    datetime_q: datetime
    note: Optional[str] = None
    doctor_report: Optional[str] = None
    doctor_note: Optional[str] = None

class ClinicAppointment(BaseModel):
    """
    Модель данных о приеме в клинике.

    Атрибуты:
        id (int): Уникальный идентификатор записи.
        patient_id (int): Идентификатор пациента.
        doctor_id (int): Идентификатор врача.
        datetime_q (str): Дата и время приема.
        note (Optional[str]): Примечание.
        doctor_report (Optional[str]): Отчет врача.
        doctor_note (Optional[str]): Заметка врача.
        doctor_full_name (Optional[str]): Полное имя врача.
    """
    id: int
    patient_id: int
    doctor_id: int
    datetime_q: str
    note: Optional[str] = None
    doctor_report: Optional[str] = None
    doctor_note: Optional[str] = None
    doctor_full_name: Optional[str] = None

    class Config:
        orm_mode = True

class AppointmentUpdate(BaseModel):
    doctor_report: str
    doctor_note: str


class Vvk(BaseModel):
    """
    Модель данных о ВВК.

    Атрибуты:
        id (int): Уникальный идентификатор записи.
        patient_id (int): Идентификатор пациента.
        vvk_date (date): Дата ВВК.
        vvk_number (str): Номер ВВК.
        conclusion (str): Заключение ВВК.
    """
    id: int
    patient_id: int
    vvk_date: date
    vvk_number: str
    conclusion: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class VvkCreate(BaseModel):
    """
    Модель для создания данных о ВВК.

    Атрибуты:
        patient_id (int): Идентификатор пациента.
        vvk_date (date): Дата ВВК.
        vvk_number (str): Номер ВВК.
        conclusion (str): Заключение ВВК.
    """
    patient_id: int
    vvk_date: date
    vvk_number: str
    conclusion: str

class DoctorsOfTheClinic(BaseModel):
    """
    Модель данных о врачах клиники.

    Атрибуты:
        id (int): Уникальный идентификатор записи.
        doctor_type (str): Тип врача.
        full_name (str): Полное имя врача.
        cabinet (str): Кабинет врача.
    """
    id: int
    doctor_type: str
    full_name: str
    cabinet: str

    class Config:
        orm_mode = True

class PatientUpdate(BaseModel):
    """
    Модель для обновления данных о пациенте.

    Атрибуты:
        full_name (str): Полное имя пациента.
        directed (Optional[str]): Направление.
        birthday (Optional[str]): Дата рождения.
        address (Optional[str]): Адрес.
        policy_CMI (Optional[str]): Полис ОМС.
        snils (Optional[str]): СНИЛС.
        document (Optional[str]): Документ.
        military_unit (Optional[str]): Воинская часть.
        military_rank (Optional[str]): Воинское звание.
        belonging (Optional[str]): Принадлежность.
        hostilities (Optional[bool]): Участие в боевых действиях.
        personal_number (Optional[str]): Личный номер.
        military_commissariat (Optional[str]): Военный комиссариат.
        military_district (Optional[str]): Военный округ.
        phone_number (Optional[str]): Номер телефона.
        card_number (Optional[str]): Номер карты.
        patient_info (Optional[str]): Информация о пациенте.
        medical_type (Optional[str]): Тип медицинской помощи.
    """
    full_name: str
    directed: Optional[str] = None
    birthday: Optional[str] = None
    address: Optional[str] = None
    policy_CMI: Optional[str] = None
    snils: Optional[str] = None     
    document: Optional[str] = None
    military_unit: Optional[str] = None
    military_rank: Optional[str] = None
    belonging: Optional[str] = None
    hostilities: Optional[bool] = None
    personal_number: Optional[str] = None
    military_commissariat: Optional[str] = None
    military_district: Optional[str] = None
    phone_number: Optional[str] = None
    card_number: Optional[str] = None
    patient_info: Optional[str] = None
    medical_type: Optional[str] = None

class AppointmentsResponse(BaseModel):
    """
    Модель для ответа по назначениям.

    Атрибуты:
        active_appointments (List[ClinicAppointment]): Список активных назначений.
        inactive_appointments (List[ClinicAppointment]): Список неактивных назначений.
    """
    active_appointments: List[ClinicAppointment]
    inactive_appointments: List[ClinicAppointment]

class UpdatePatientData(BaseModel):
    full_name: Optional[str]
    directed: Optional[str]
    birthday: Optional[datetime]
    address: Optional[str]
    policy_CMI: Optional[str]
    snils: Optional[str]
    document: Optional[str]
    military_unit: Optional[str]
    military_rank: Optional[str]
    belonging: Optional[str]
    hostilities: Optional[bool]
    personal_number: Optional[str]
    military_commissariat: Optional[str]
    military_district: Optional[str]
    phone_number: Optional[str]
    card_number: Optional[str]
    patient_info: Optional[str]
    medical_type: Optional[str]
    vkk_info: Optional[str]
    hospitalization_info: Optional[str]
    appointments: Optional[List[dict]]
    hospitalizations: Optional[List[dict]]
    vvks: Optional[List[dict]]
