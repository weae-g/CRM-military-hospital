from ...model.database.database import SessionLocal
from ...model.pacient_hospital import models, schemas, old_models
from typing import List, Tuple, Optional, Dict, Union
from datetime import datetime, date, timedelta
from pytz import timezone
import pandas as pd
MIN_CHAR_COUNT = 3  # Минимальное количество символов для поля, чтобы оно считалось заполненным

# Устанавливаем временную зону Москвы
moscow_tz = timezone('Europe/Moscow')

def format_datetime(value: datetime, format: str = "%d.%m.%Y %H:%M:%S") -> str:
    """
    Форматирует объект datetime в строку по заданному формату.

    Параметры:
    value (datetime): Объект datetime, который нужно отформатировать.
    format (str): Формат строки, в который будет преобразован datetime (по умолчанию "%d.%m.%Y %H:%M:%S").

    Возвращает:
    str: Отформатированная строка. Если значение `value` равно None, возвращается пустая строка.
    """
    if value is None:
        return ""
    return value.strftime(format)

def get_moscow_time() -> datetime:
    """
    Получает текущее время в Москве.

    Возвращает:
    datetime: Текущее время в Москве в формате datetime.
    """
    return datetime.now(moscow_tz)

def remove_tzinfo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Удаляет информацию о временной зоне из всех столбцов datetime в DataFrame и преобразует даты в строки.

    Параметры:
    df (pd.DataFrame): DataFrame, из которого нужно удалить информацию о временной зоне и преобразовать даты.

    Возвращает:
    pd.DataFrame: DataFrame с удаленной информацией о временной зоне и преобразованными столбцами datetime в строки.
    """
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # Убираем временную зону
            df[col] = df[col].apply(lambda x: x.tz_localize(None) if pd.notnull(x) and x.tzinfo is not None else x)
            # Преобразуем в строку с заданным форматом
            df[col] = df[col].apply(lambda x: x.strftime("%d.%m.%Y") if pd.notnull(x) else x)
    return df

def remove_tzinfo_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Преобразует все столбцы datetime в DataFrame в московскую временную зону
    и удаляет информацию о временной зоне, возвращая их как даты.

    Параметры:
    df (pd.DataFrame): DataFrame, в котором нужно преобразовать столбцы datetime.

    Возвращает:
    pd.DataFrame: DataFrame с преобразованными столбцами datetime без временной зоны.
    """
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_convert('Europe/Moscow')  # Преобразование в московскую временную зону
            df[col] = df[col].dt.tz_localize(None)  # Удаление информации о временной зоне
            df[col] = df[col].dt.date  # Преобразование в тип date

    return df


# Список символов, которые будут игнорироваться при проверке заполненности полей
EXCLUDED_CHARACTERS = [' ', '-', '_', '.']


def remove_excluded_characters(value: str) -> str:
    """
    Удаляет исключенные символы из строки.

    Args:
        value (str): Входная строка.

    Returns:
        str: Строка без исключенных символов.
    """
    for char in EXCLUDED_CHARACTERS:
        value = value.replace(char, '')
    return value

def check_field_completeness(value: Union[str, date], field_name: str, min_char_count: int = MIN_CHAR_COUNT) -> bool:
    """
    Проверяет заполненность поля. Для строк проверяет количество символов, для дат — всегда считается заполненным.

    Args:
        value (Union[str, date]): Значение поля.
        field_name (str): Имя поля.
        min_char_count (int): Минимальное количество символов для строки, чтобы поле считалось заполненным.

    Returns:
        bool: True, если поле считается заполненным, иначе False.
    """
    if isinstance(value, date):
        return True  # Дата всегда считается заполненной
    elif isinstance(value, str):
        value = remove_excluded_characters(value)
        return len(value) >= min_char_count
    else:
        return False

def check_patient_data_completeness(passport_data: models.PassportData) -> Tuple[List[str], float]:
    incomplete_fields = []

    # Поля для PassportData
    passport_fields = [
        'full_name', 'birthday_date', 'personal_data', 'military_rank',
        'directions', 'date_of_illness', 'address', 'military_unit',
        'history_number', 'phone_number', 'branch', 'service_basis',
        'personal_document'
    ]

    # Проверка полей модели PassportData
    for field in passport_fields:
        value = getattr(passport_data, field, None)
        if not check_field_completeness(value, field):
            incomplete_fields.append(field)

    # Поля для HospitalData
    hospital_fields = [
        'vk_urgent_call_date', 'vk_call_up_date', 'district',
        'diagnosis_upon_admission', 'final_diagnosis', 'ICD',
        'character_of_the_hospital', 'reason_for_departure',
        'vvk_decision', 'anamnesis', 'expert_diagnosis',
        'diagnosis_according_to_form_one_hundred', 'therapist'
    ]

    # Проверка связанных госпитальных данных
    for hospital_data in passport_data.hospital_records:
        for field in hospital_fields:
            value = getattr(hospital_data, field, None)
            if not check_field_completeness(value, field):
                incomplete_fields.append(f"{field} (hospital_record)")

    # Общий список полей для расчета процента 
    total_fields_count = len(passport_fields) + len(hospital_fields) * len(passport_data.hospital_records)
    filled_fields_count = total_fields_count - len(incomplete_fields)
    
    completeness_percentage = (filled_fields_count / total_fields_count) * 100 if total_fields_count else 100


    return incomplete_fields, completeness_percentage

def check_completeness_by_branch(passport_data_list: List[models.PassportData]) -> Dict[str, float]:
    """
    Проверяет полноту данных по филиалам.

    Args:
        passport_data_list (List[models.PassportData]): Список данных паспортов пациентов.

    Returns:
        Dict[str, float]: Словарь с процентами полноты данных по каждому филиалу.
    """
    branch_completeness = {}
    branch_counts = {}

    for passport_data in passport_data_list:
        branch = passport_data.branch
        if branch not in branch_completeness:
            branch_completeness[branch] = 0
            branch_counts[branch] = 0
        
        _, completeness_percentage = check_patient_data_completeness(passport_data)
        branch_completeness[branch] += completeness_percentage
        branch_counts[branch] += 1

    for branch in branch_completeness:
        branch_completeness[branch] /= branch_counts[branch]

    return branch_completeness
