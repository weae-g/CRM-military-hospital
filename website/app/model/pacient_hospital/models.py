from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, Boolean, Time
from ..database.database import Base
from sqlalchemy import event

from sqlalchemy.orm import relationship

from datetime import datetime
from pytz import timezone

# Устанавливаем временную зону Москвы
moscow_tz = timezone('Europe/Moscow')

# Функция для получения текущего времени в Москве
def get_moscow_time():
    return datetime.now(moscow_tz)

class HospitalRecord(Base):
    """
    Модель данных для записи о госпитализации.

    Attributes:
        id (int): Уникальный идентификатор записи.
        doctor_id (int): ID врача из таблицы doctors_of_the_clinic.
        patient_id (int): ID пациента из таблицы passport_data.
        date (time): Время записи.
        note (text): Записка, для.
    """
    __tablename__ = 'hospital_record'
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors_of_the_clinic.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('passport_data.id'), nullable=False)
    date = Column(Time)
    note = Column(Text)

    doctor = relationship("DoctorsOfTheClinic", back_populates="hospital_record_apply")
    patient = relationship("PassportData", back_populates="hospital_record_apply")


class HospitalData(Base):
    """
    Модель данных для информации о госпитализации пациента.

    Attributes:
        id (int): Уникальный идентификатор записи.
        patient_id (int): ID пациента из таблицы PassportData.
        vk_urgent_call_date (str): Дата срочного вызова (VK).
        vk_call_up_date (str): Дата вызова (VK).
        district (str): Район.
        diagnosis_upon_admission (str): Диагноз при поступлении.
        final_diagnosis (str): Конечный диагноз.
        ICD (str): Международный классификатор болезней (ICD).
        character_of_the_hospital (str): Характер госпитализации.
        reason_for_departure (str): Причина выбытия.
        vvk_decision (str): Решение ВВК.
        certificate_of_injury (bool): Наличие справки о травме.
        medical_record (bool): Наличие медицинской карты.
        food_certificate (bool): Наличие справки на питание.
        sick_leave (bool): Наличие больничного листа.
        entered_after_participating_in_hostilities (bool): Поступление после участия в боевых действиях.
        suitability_category (bool): Категория годности.
        anamnesis (str): Анамнез.
        severity_of_injury (bool): Тяжесть травмы.
        expert_diagnosis (str): Экспертный диагноз.
        diagnosis_according_to_form_one_hundred (str): Диагноз по форме 100.
        therapist (str): Лечащий врач.

    Relationships:
        patient (PassportData): Связь с таблицей PassportData.
    """
    __tablename__ = 'hospital_data'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('passport_data.id'), nullable=False)
    vk_urgent_call_date = Column(Text)
    vk_call_up_date = Column(Text)
    district = Column(Text)
    diagnosis_upon_admission = Column(Text)
    final_diagnosis = Column(Text)
    ICD = Column(Text)
    character_of_the_hospital = Column(Text)
    reason_for_departure = Column(Text)
    vvk_decision = Column(Text)
    certificate_of_injury = Column(Boolean)
    medical_record = Column(Boolean)
    food_certificate = Column(Boolean)
    sick_leave = Column(Boolean)
    entered_after_participating_in_hostilities = Column(Boolean)
    suitability_category = Column(Boolean)
    anamnesis = Column(Text)
    severity_of_injury = Column(Boolean)
    expert_diagnosis = Column(Text)
    diagnosis_according_to_form_one_hundred = Column(Text)
    therapist = Column(Text)

    patient = relationship("PassportData", back_populates="hospital_records")


class PatientMovement(Base):
    """
    Модель данных для отслеживания движений пациента между отделениями.

    Attributes:
        id (int): Уникальный идентификатор записи.
        patient_id (int): ID пациента из таблицы PassportData.
        department (str): Отделение.
        event_type (str): Тип события (например, "Прием на госпитализацию").
        event_date (datetime): Дата и время события.
        destination_department (str): Целевое отделение (если есть).
        note (str): Примечание.

    Relationships:
        patient (PassportData): Связь с таблицей PassportData.
    """
    __tablename__ = 'patient_movements'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('passport_data.id'), nullable=False)
    department = Column(Text, nullable=False)
    event_type = Column(Text, nullable=False)  
    event_date = Column(DateTime, default=datetime.now(), nullable=False)
    destination_department = Column(Text) 
    note = Column(Text)
    patient = relationship("PassportData", back_populates="movements")

class VvkHospital(Base):
    """
    Модель данных для информации о госпитализации пациента на ВВК.

    Attributes:
        id (int): Уникальный идентификатор записи.
        vvk_number (str): Номер ВВК.
        vvk_date (datetime): Дата ВВК.
        conclusion (str): Заключение ВВК.
        patient_id (int): ID пациента из таблицы PassportData.

    Relationships:
        patient (PassportData): Связь с таблицей PassportData.
    """
    __tablename__ = "vvk_hospital"
    id = Column(Integer, primary_key=True)
    vvk_number = Column(Text, nullable=False)
    vvk_date = Column(DateTime, nullable=False)
    conclusion = Column(Text, nullable=False)
    date_of_dispatch = Column(DateTime, nullable=True)
    date_of_approval = Column(DateTime, nullable=True)
    
    patient_id = Column(Integer, ForeignKey('passport_data.id'), nullable=False)
    patient = relationship("PassportData", back_populates="vvk")

class CertificateOfInjury(Base):
    """
    Модель данных для справки о травме пациента.

    Attributes:
        id (int): Уникальный идентификатор записи.
        patient_id (int): ID пациента из таблицы PassportData.
        certificate_injury_date (datetime): Дата выдачи справки о травме.
        load_date (datetime): Дата загрузки.
        injury_number (str): Номер травмы (если есть).

    Relationships:
        patient (PassportData): Связь с таблицей PassportData.
    """
    __tablename__ = "certificate_of_injury"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('passport_data.id'), nullable=False)
    certificate_injury_date = Column(DateTime, nullable=False)
    load_date = Column(DateTime)
    injury_number = Column(Text, nullable=True)
    patient = relationship("PassportData", back_populates="injury")

class CertificateOfSeverity(Base):
    """
    Модель данных для справки о тяжести состояния пациента.

    Attributes:
        id (int): Уникальный идентификатор записи.
        patient_id (int): ID пациента из таблицы PassportData.
        severity_number (str): Номер справки о тяжести состояния.
        severity_date (datetime): Дата выдачи справки о тяжести состояния.
        approval_date (datetime): Дата утверждения (если есть).
        approval_number (str): Номер утверждения (если есть).

    Relationships:
        patient (PassportData): Связь с таблицей PassportData.
    """
    __tablename__ = "certificate_of_severity"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('passport_data.id'), nullable=False)
    severity_number = Column(Text, nullable=False)
    severity_date = Column(DateTime, nullable=False)
    approval_date = Column(DateTime, nullable=True)
    approval_number = Column(Text, nullable=True)
    patient = relationship("PassportData", back_populates="severity")

class PassportData(Base):
    """
    Модель данных для паспортных данных пациента.

    Attributes:
        id (int): Уникальный идентификатор записи.
        full_name (str): Полное имя пациента.
        birthday_date (datetime): Дата рождения.
        personal_data (str): Личные данные (например, паспортные данные).
        military_rank (str): Воинское звание.
        current_time (datetime): Текущее время (может использоваться для записи времени создания).
        directions (str): Направления (например, для лечения).
        date_of_illness (datetime): Дата заболевания.
        address (str): Адрес.
        military_unit (str): Воинская часть.
        history_number (str): Номер истории болезни.
        phone_number (str): Номер телефона.
        branch (str): Военная часть.
        service_basis (str): Основание для обслуживания.
        personal_document (str): Личный документ (например, паспорт).
        nature_of_hospitalization (str): Характер госпитализации.
        first_diagnosis (str): Первоначальный диагноз.
        after_hostilities (bool): Поступление после участия в боевых действиях.

    Relationships:
        severity (list[CertificateOfSeverity]): Связь с таблицей CertificateOfSeverity.
        injury (list[CertificateOfInjury]): Связь с таблицей CertificateOfInjury.
        vvk (list[VvkHospital]): Связь с таблицей VvkHospital.
        movements (list[PatientMovement]): Связь с таблицей PatientMovement.
        hospital_records (list[HospitalData]): Связь с таблицей HospitalData.
    """
    __tablename__ = 'passport_data'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)
    birthday_date = Column(DateTime)
    personal_data = Column(Text)
    military_rank = Column(Text)
    current_time = Column(DateTime, nullable=False)
    directions = Column(Text)
    date_of_illness = Column(DateTime)
    address = Column(Text)
    military_unit = Column(Text)
    history_number = Column(Text)
    phone_number = Column(Text)
    branch = Column(Text)
    service_basis = Column(Text)
    personal_document = Column(Text)
    nature_of_hospitalization = Column(Text)
    first_diagnosis = Column(Text)
    after_hostilities = Column(Boolean)
    unit_commander = Column(Text)

    severity = relationship("CertificateOfSeverity", back_populates="patient", cascade="all, delete-orphan")
    injury = relationship("CertificateOfInjury", back_populates="patient", cascade="all, delete-orphan")
    vvk = relationship("VvkHospital", back_populates="patient", cascade="all, delete-orphan")
    movements = relationship("PatientMovement", back_populates="patient", cascade="all, delete-orphan")
    hospital_records = relationship("HospitalData", back_populates="patient", cascade="all, delete-orphan")
    hospital_record_apply = relationship("HospitalRecord", back_populates="patient")


def log_patient_admission(mapper, connection, target):
    """
    Логирование при создании нового пациента и добавление начальной записи в таблицу HospitalData.

    При создании нового пациента функция добавляет запись о приеме пациента на госпитализацию в таблицу 
    PatientMovement и создает начальную запись в таблице HospitalData с основными данными пациента.

    Args:
        mapper (Mapper): SQLAlchemy mapper, который отвечает за отображение модели данных.
        connection (Connection): Соединение с базой данных.
        target (Patient): Объект пациента, для которого создаются записи.

    Returns:
        None
    """
    # Логирование приема пациента на госпитализацию
    new_movement = PatientMovement(
        patient_id=target.id,
        department=target.branch,
        event_type='Прием на госпитализацию',
        event_date=get_moscow_time(),  # Получение текущего времени по московскому времени
        note=None
    )
    connection.execute(
        PatientMovement.__table__.insert(),
        {
            'patient_id': new_movement.patient_id,
            'department': new_movement.department,
            'event_type': new_movement.event_type,
            'event_date': new_movement.event_date,
            'note': new_movement.note
        }
    )

    # Добавление начальной записи в HospitalData
    new_hospital_data = HospitalData(
        patient_id=target.id,
        vk_urgent_call_date=None,  # Дата срочного вызова ВК
        vk_call_up_date=None,      # Дата вызова ВК
        district=None,             # Район
        diagnosis_upon_admission=None,  # Диагноз при поступлении
        final_diagnosis=None,      # Окончательный диагноз
        ICD=None,                  # Код по МКБ
        character_of_the_hospital=None, # Характер госпитализации
        reason_for_departure=None, # Причина выбытия
        vvk_decision=None,         # Решение ВВК
        certificate_of_injury=False, # Наличие справки о травме
        medical_record=False,      # Наличие медицинской карты
        food_certificate=False,    # Наличие справки о питании
        sick_leave=False,          # Наличие больничного листа
        entered_after_participating_in_hostilities=False, # Вступил после участия в боевых действиях
        suitability_category=False, # Категория годности
        anamnesis=None,            # Анамнез
        expert_diagnosis=None,     # Экспертное заключение
        diagnosis_according_to_form_one_hundred=None,  # Диагноз по форме 100
        therapist=None             # Терапевт
    )
    connection.execute(
        HospitalData.__table__.insert(),
        {
            'patient_id': new_hospital_data.patient_id,
            'vk_urgent_call_date': new_hospital_data.vk_urgent_call_date,
            'vk_call_up_date': new_hospital_data.vk_call_up_date,
            'district': new_hospital_data.district,
            'diagnosis_upon_admission': new_hospital_data.diagnosis_upon_admission,
            'final_diagnosis': new_hospital_data.final_diagnosis,
            'ICD': new_hospital_data.ICD,
            'character_of_the_hospital': new_hospital_data.character_of_the_hospital,
            'reason_for_departure': new_hospital_data.reason_for_departure,
            'vvk_decision': new_hospital_data.vvk_decision,
            'certificate_of_injury': new_hospital_data.certificate_of_injury,
            'medical_record': new_hospital_data.medical_record,
            'food_certificate': new_hospital_data.food_certificate,
            'sick_leave': new_hospital_data.sick_leave,
            'diagnosis_according_to_form_one_hundred': new_hospital_data.diagnosis_according_to_form_one_hundred,
            'suitability_category': new_hospital_data.suitability_category,
            'expert_diagnosis': new_hospital_data.expert_diagnosis,
            'anamnesis': new_hospital_data.anamnesis,
            'therapist': new_hospital_data.therapist
        }
    )


def log_patient_update(mapper, connection, target):
    """ Логирование при обновлении данных пациента.

    Эта функция предназначена для регистрации изменений в данных пациента,
    таких как изменение статуса или отделения. Реализация зависит от конкретных
    требований бизнес-логики приложения.

    Args:
        mapper: Маппер SQLAlchemy.
        connection: Соединение с базой данных.
        target: Объект, который был обновлен (экземпляр PassportData).

    Returns:
        None

    Raises:
        SQLAlchemyError: Если возникает ошибка при взаимодействии с базой данных.

    Notes:
        Для логики обновления можно использовать условия и проверки на изменения
        определенных полей, чтобы регистрировать только значимые обновления.

    """
    # В этой функции можно добавить логику для различения типов обновлений
    # Например, если статус или отделение изменилось, регистрировать перевод
    pass  # Наполните функцию в соответствии с логикой

# Подключение слушателей к событиям
event.listen(PassportData, 'after_insert', log_patient_admission)
event.listen(PassportData, 'after_update', log_patient_update)
