from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HospitalDataCreate(BaseModel):
    """
    Модель для создания данных о пациенте в больнице.
    
    Атрибуты:
        patient_id (int): Идентификатор пациента.
        vk_urgent_call_date (Optional[str]): Дата экстренного вызова (может быть None).
        vk_call_up_date (Optional[str]): Дата вызова (может быть None).
        district (Optional[str]): Район (может быть None).
        diagnosis_upon_admission (Optional[str]): Диагноз при поступлении (может быть None).
        final_diagnosis (Optional[str]): Окончательный диагноз (может быть None).
        ICD (Optional[str]): Код по МКБ (может быть None).
        character_of_the_hospital (Optional[str]): Характер госпитализации (может быть None).
        reason_for_departure (Optional[str]): Причина выписки (может быть None).
        vvk_decision (Optional[str]): Решение ВВК (может быть None).
        certificate_of_injury (Optional[bool]): Наличие справки о травме (может быть None).
        medical_record (Optional[bool]): Наличие медицинской карты (может быть None).
        food_certificate (Optional[bool]): Наличие справки о питании (может быть None).
        sick_leave (Optional[bool]): Наличие больничного листа (может быть None).
        entered_after_participating_in_hostilities (Optional[bool]): Поступил после участия в боевых действиях (может быть None).
        did_not_reach_the_part (Optional[bool]): Не дошел до части (может быть None).
        anamnesis (Optional[str]): Анамнез (может быть None).
        severity_of_injury (Optional[str]): Степень тяжести травмы (может быть None).
    """
    patient_id: int
    vk_urgent_call_date: Optional[str] = None
    vk_call_up_date: Optional[str] = None
    district: Optional[str] = None
    diagnosis_upon_admission: Optional[str] = None
    final_diagnosis: Optional[str] = None
    ICD: Optional[str] = None
    character_of_the_hospital: Optional[str] = None
    reason_for_departure: Optional[str] = None
    vvk_decision: Optional[str] = None
    certificate_of_injury: Optional[bool] = None
    medical_record: Optional[bool] = None
    food_certificate: Optional[bool] = None
    sick_leave: Optional[bool] = None
    entered_after_participating_in_hostilities: Optional[bool] = None
    did_not_reach_the_part: Optional[bool] = None
    anamnesis: Optional[str] = None
    severity_of_injury: Optional[str] = None

class HospitalDataUpdate(HospitalDataCreate):
    """
    Модель для обновления данных о пациенте в больнице.
    
    Наследует все атрибуты от HospitalDataCreate.
    """
    pass

class PatientMovementCreate(BaseModel):
    """
    Модель для создания данных о перемещении пациента.

    Атрибуты:
        patient_id (int): Идентификатор пациента.
        department (str): Отделение, в котором находится пациент.
        event_type (str): Тип события (например, перевод, поступление).
        event_date (datetime): Дата события.
        destination_department (Optional[str]): Отделение назначения (может быть None).
    """
    patient_id: int
    department: str
    event_type: str
    event_date: datetime
    destination_department: Optional[str] = None

class PatientMovementUpdate(BaseModel):
    """
    Модель для обновления данных о перемещении пациента.

    Атрибуты:
        department (Optional[str]): Отделение, в котором находится пациент (может быть None).
        event_type (Optional[str]): Тип события (может быть None).
        event_date (Optional[datetime]): Дата события (может быть None).
        destination_department (Optional[str]): Отделение назначения (может быть None).
    """
    department: Optional[str] = None
    event_type: Optional[str] = None
    event_date: Optional[datetime] = None
    destination_department: Optional[str] = None

class VvkHospitalCreate(BaseModel):
    """
    Модель для создания данных о решении ВВК.

    Атрибуты:
        patient_id (int): Идентификатор пациента.
        vvk_number (str): Номер ВВК.
        vvk_date (datetime): Дата ВВК.
        conclusion (str): Заключение ВВК.
    """
    patient_id: int
    vvk_number: str
    vvk_date: datetime
    conclusion: str

class DepartmentStats(BaseModel):
    """
    Модель для статистики по отделению.

    Атрибуты:
        department (str): Название отделения.
        admissions (int): Количество поступлений.
        discharges (int): Количество выписок.
        transfers (int): Количество переводов.
        current_count (int): Текущий контингент.
        load_percentage (float): Процент загрузки.
    """
    department: str
    admissions: int
    discharges: int
    transfers: int
    current_count: int
    load_percentage: float

class PassportDataBase(BaseModel):
    """
    Базовая модель данных паспорта.

    Атрибуты:
        full_name (str): ФИО.
        birthday_date (Optional[datetime]): Дата рождения (может быть None).
        personal_data (Optional[str]): Личные данные (может быть None).
        military_rank (Optional[str]): Воинское звание (может быть None).
        directions (Optional[str]): Направления (может быть None).
        date_of_illness (Optional[datetime]): Дата заболевания (может быть None).
        address (Optional[str]): Адрес (может быть None).
        military_unit (Optional[str]): Воинская часть (может быть None).
        history_number (Optional[str]): Номер истории болезни (может быть None).
        phone_number (Optional[str]): Телефонный номер (может быть None).
        branch (Optional[str]): Подразделение (может быть None).
        service_basis (Optional[str]): Основание для службы (может быть None).
        personal_document (Optional[str]): Личный документ (может быть None).
    """
    full_name: str
    birthday_date: Optional[datetime] = None
    personal_data: Optional[str] = None
    military_rank: Optional[str] = None
    directions: Optional[str] = None
    date_of_illness: Optional[datetime] = None
    address: Optional[str] = None
    military_unit: Optional[str] = None
    history_number: Optional[str] = None
    phone_number: Optional[str] = None
    branch: Optional[str] = None
    service_basis: Optional[str] = None
    personal_document: Optional[str] = None

class PassportDataCreate(PassportDataBase):
    """
    Модель для создания данных паспорта.

    Наследует все атрибуты от PassportDataBase.
    """
    pass

class PassportDataUpdate(PassportDataBase):
    """
    Модель для обновления данных паспорта.

    Наследует все атрибуты от PassportDataBase.
    """
    pass

class CertificateOfSeverity(BaseModel):
    """
    Модель для данных о справке о степени тяжести.

    Атрибуты:
        severity_number (str): Номер справки о степени тяжести.
        severity_date (datetime): Дата справки о степени тяжести.
        approval_date (datetime): Дата утверждения.
        approval_number (str): Номер утверждения.
    """
    severity_number: str
    severity_date: datetime
    approval_date: datetime
    approval_number: str

class CertificateOfInjury(BaseModel):
    """
    Модель для данных о справке о травме.

    Атрибуты:
        certificate_injury_date (datetime): Дата справки о травме.
        load_date (datetime): Дата загрузки.
        injury_number (str): Номер травмы.
        patient_id (int): Идентификатор пациента.
    """
    certificate_injury_date: datetime
    load_date: datetime
    injury_number: str
    patient_id: int

class CertificateOfSeverityUpdate(BaseModel):
    """
    Модель для обновления данных о справке о степени тяжести.

    Атрибуты:
        severity_number (Optional[str]): Номер справки о степени тяжести (может быть None).
        severity_date (Optional[datetime]): Дата справки о степени тяжести (может быть None).
        approval_date (Optional[datetime]): Дата утверждения (может быть None).
        approval_number (Optional[str]): Номер утверждения (может быть None).
        patient_id (Optional[int]): Идентификатор пациента (может быть None).
    """
    severity_number: Optional[str] = None
    severity_date: Optional[datetime] = None
    approval_date: Optional[datetime] = None
    approval_number: Optional[str] = None
    patient_id: Optional[int] = None

class CertificateOfSeverityUpdate(BaseModel):
    """
    Модель для обновления данных о справке о травме.

    Атрибуты:
        certificate_injury_date (datetime): Дата справки о травме.
        load_date (datetime): Дата загрузки.
        injury_number (str): Номер травмы.
        patient_id (Optional[int]): Идентификатор пациента (может быть None).
    """
    severity_number: Optional[str] = None
    severity_date: Optional[datetime] = None
    approval_date: Optional[datetime] = None
    approval_number: Optional[str] = None
    patient_id: Optional[int] = None

class CertificateOfInjuryUpdate(BaseModel):
    """
    Модель данных паспорта с идентификатором.

    Атрибуты:
        id (int): Уникальный идентификатор записи.
    """
    certificate_injury_date: datetime
    load_date: datetime
    injury_number: str
    patient_id: Optional[int] = None

class PassportData(PassportDataBase):
    """
        Настройки конфигурации Pydantic для работы с ORM.
        Включает поддержку преобразования данных из ORM-моделей.
    """
    id: int

    class Config:
        orm_mode = True
