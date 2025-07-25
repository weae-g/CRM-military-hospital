import tempfile
import zipfile
from fastapi import FastAPI, Request, APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from ...model.pacient_hospital import models, old_models

from sqlalchemy.orm import Session
import pandas as pd
import os
from dotenv import load_dotenv
from ...model.user.auth import authorize_request
from .._utils.documents_utils import fill_template, docs_dir, templates
from .._utils.read_excel_utils import read_excel, read_excel_ds
from .._utils.db_utils import get_db 

# Загрузить переменные окружения из файла .env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), "app", ".env"))

# Путь к файлам
FILE_PATH_RKB = os.getenv("file_path_rkb")
FILE_PATH_GKB = os.getenv("file_path_gkb")
FILE_PATH_GVV = os.getenv("file_path_gvv")
FILE_PATH_DAY_HOSPITAL = os.getenv("file_path_day_hospital")
FILE_PATH_CLINIC = os.getenv('file_path_clinic')

current_dir = os.path.dirname(os.path.abspath(__file__))

router = APIRouter()

@router.get("/clinic", response_class=HTMLResponse)
async def index(request: Request):
    """
    Отображение таблицы данных из Excel-файла для клиники.

    Этот эндпоинт загружает данные из Excel-файла для клиники и отображает их на веб-странице
    с использованием HTML-шаблона `clinic_table.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу данных из Excel-файла.
    """
    data = read_excel_ds(FILE_PATH_CLINIC, True)
    return templates.TemplateResponse("other/clinic_table.html", {"request": request, "data": data})

@router.get("/ds", response_class=HTMLResponse)
async def index(request: Request):
    """
    Отображение таблицы данных из Excel-файла для дневной госпитализации.

    Этот эндпоинт загружает данные из Excel-файла для дневной госпитализации и отображает их 
    на веб-странице с использованием HTML-шаблона `day_hospitalization.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу данных из Excel-файла.
    """
    data = read_excel_ds(FILE_PATH_DAY_HOSPITAL, True)
    return templates.TemplateResponse("other/day_hospitalization.html", {"request": request, "data": data})

@router.get("/rkb_drawn", response_class=HTMLResponse)
async def index(request: Request):
    """
    Отображение таблицы данных из Excel-файла для РКБ с пометками о нарушениях.

    Этот эндпоинт загружает данные из Excel-файла для РКБ, проверяет на наличие нарушений,
    и отображает их на веб-странице с использованием HTML-шаблона `drawn_table.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу данных из Excel-файла с пометками нарушений.
    """
    data, has_violation = read_excel(FILE_PATH_RKB)
    return templates.TemplateResponse("other/drawn_table.html", {"request": request, "data": data, "has_violation": has_violation})

@router.get("/rkb", response_class=HTMLResponse)
async def index(request: Request):
    """
    Отображение таблицы данных из Excel-файла для РКБ без пометок о нарушениях.

    Этот эндпоинт загружает данные из Excel-файла для РКБ, проверяет на наличие нарушений,
    и отображает их на веб-странице с использованием HTML-шаблона `template_table.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу данных из Excel-файла.
    """

    data, has_violation = read_excel(FILE_PATH_RKB)
    return templates.TemplateResponse("other/template_table.html", {
        "request": request,
        "data": data,
        "has_violation": has_violation,
        "title": "Сведения по пациентам РКБ",
        "download_link": "/otx/rkb/download"
    })

from datetime import datetime
@router.get("/rkb/download")
async def download_rkb_file(request: Request):
    """
    Отправка файла для скачивания для РКБ с указанием текущей даты и времени в названии файла.
    
    Args:
        request (Request): Объект запроса FastAPI.
        
    Returns:
        FileResponse: Файл для скачивания.
    """
    file_path = FILE_PATH_RKB  # Укажите путь к файлу, который хотите скачать
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    filename = f"РКБ_{current_time}.xlsx"
    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=filename)

@router.get("/gkb7/download")
async def download_gkb7_file(request: Request):
    """
    Отправка файла для скачивания для ГКБ 7 с указанием текущей даты и времени в названии файла.
    
    Args:
        request (Request): Объект запроса FastAPI.
        
    Returns:
        FileResponse: Файл для скачивания.
    """
    file_path = FILE_PATH_GKB  # Укажите путь к файлу, который хотите скачать
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    filename = f"ГКБ7_{current_time}.xlsx"
    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=filename)

@router.get("/gkb7", response_class=HTMLResponse)
async def index(request: Request):
    """
    Отображение таблицы данных из Excel-файла для ГКБ 7 без пометок о нарушениях.

    Этот эндпоинт загружает данные из Excel-файла для ГКБ 7, проверяет на наличие нарушений,
    и отображает их на веб-странице с использованием HTML-шаблона `template_table.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу данных из Excel-файла.
    """
    data, has_violation = read_excel(FILE_PATH_GKB)
    return templates.TemplateResponse("other/template_table.html", {
        "request": request,
        "data": data,
        "has_violation": has_violation,
        "title": "Сведения по пациентам ГКБ7",
        "download_link": "/otx/gkb7/download"
    })

@router.get("/gvv/download")
async def download_gvv_file(request: Request):
    """
    Отправка файла для скачивания для ГКБ 7 с указанием текущей даты и времени в названии файла.
    
    Args:
        request (Request): Объект запроса FastAPI.
        
    Returns:
        FileResponse: Файл для скачивания.
    """
    file_path = FILE_PATH_GVV  # Укажите путь к файлу, который хотите скачать
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    filename = f"ГдВВ_{current_time}.xlsx"
    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=filename)

@router.get("/gvv", response_class=HTMLResponse)
async def index(request: Request):
    """
    Отображение таблицы данных из Excel-файла для ГКБ 7 без пометок о нарушениях.

    Этот эндпоинт загружает данные из Excel-файла для ГКБ 7, проверяет на наличие нарушений,
    и отображает их на веб-странице с использованием HTML-шаблона `template_table.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу данных из Excel-файла.
    """
    data, has_violation = read_excel(FILE_PATH_GVV)
    return templates.TemplateResponse("other/template_table.html", {
        "request": request,
        "data": data,
        "has_violation": has_violation,
        "title": "Сведения по пациентам ГдВВ",
        "download_link": "/otx/gvv/download"
    })

@router.get("/gvv_drawn", response_class=HTMLResponse)
async def index_gvv(request: Request):
    """
    Отображение таблицы данных из Excel-файла для ГКБ 7 с пометками о нарушениях.

    Этот эндпоинт загружает данные из Excel-файла для ГКБ 7, проверяет на наличие нарушений,
    и отображает их на веб-странице с использованием HTML-шаблона `drawn_table.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу данных из Excel-файла с пометками нарушений.
    """
    data, has_violation = read_excel(FILE_PATH_GVV)
    return templates.TemplateResponse("other/drawn_table.html", {"request": request, "data": data, "has_violation": has_violation})

@router.get("/gvv_hospitalized", response_class=HTMLResponse)
async def hospitalized_patients_gvv(request: Request):
    """
    Отображение списка пациентов ГКБ 7, которые в настоящее время находятся на госпитализации.

    Этот эндпоинт загружает данные из Excel-файла для ГКБ 7, фильтрует пациентов, у которых отсутствует дата выписки 
    (т.е. они все еще находятся на госпитализации), и отображает их на веб-странице с использованием HTML-шаблона 
    `on_hospitalization_table.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу пациентов, находящихся на госпитализации.
    """
    # Считываем данные из файлов
    data_rkb, _ = read_excel(FILE_PATH_GVV)
    
    # Фильтруем пациентов по наличию NaN в колонке "Дата выписки (убытия в часть)"
    hospitalized_patients = [
        patient for patient in data_rkb 
        if pd.isna(patient.get('Дата выписки (убытия в часть)'))
    ]

    return templates.TemplateResponse("other/on_hospitalization_table.html", {"request": request, "data": hospitalized_patients, "has_violation": False})


@router.get("/gkb7_drawn", response_class=HTMLResponse)
async def index(request: Request):
    """
    Отображение таблицы данных из Excel-файла для ГКБ 7 с пометками о нарушениях.

    Этот эндпоинт загружает данные из Excel-файла для ГКБ 7, проверяет на наличие нарушений,
    и отображает их на веб-странице с использованием HTML-шаблона `drawn_table.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу данных из Excel-файла с пометками нарушений.
    """
    data, has_violation = read_excel(FILE_PATH_GKB)
    return templates.TemplateResponse("other/drawn_table.html", {"request": request, "data": data, "has_violation": has_violation})

@router.get("/gkb7_hospitalized", response_class=HTMLResponse)
async def hospitalized_patients(request: Request):
    """
    Отображение списка пациентов ГКБ 7, которые в настоящее время находятся на госпитализации.

    Этот эндпоинт загружает данные из Excel-файла для ГКБ 7, фильтрует пациентов, у которых отсутствует дата выписки 
    (т.е. они все еще находятся на госпитализации), и отображает их на веб-странице с использованием HTML-шаблона 
    `on_hospitalization_table.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу пациентов, находящихся на госпитализации.
    """
    # Считываем данные из файлов
    data_rkb, _ = read_excel(FILE_PATH_GKB)
    
    # Фильтруем пациентов по наличию NaN в колонке "Дата выписки (убытия в часть)"
    hospitalized_patients = [
        patient for patient in data_rkb 
        if pd.isna(patient.get('Дата выписки (убытия в часть)'))
    ]

    return templates.TemplateResponse("other/on_hospitalization_table.html", {"request": request, "data": hospitalized_patients, "has_violation": False})

@router.get("/rkb_hospitalized", response_class=HTMLResponse)
async def hospitalized_patients(request: Request):
    """
    Отображение списка пациентов РКБ, которые в настоящее время находятся на госпитализации.

    Этот эндпоинт загружает данные из Excel-файла для РКБ, фильтрует пациентов, у которых отсутствует дата выписки 
    (т.е. они все еще находятся на госпитализации), и отображает их на веб-странице с использованием HTML-шаблона 
    `on_hospitalization_table.html`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница, содержащая таблицу пациентов, находящихся на госпитализации.
    """
    # Считываем данные из файлов
    data_rkb, _ = read_excel(FILE_PATH_RKB)
    
    # Фильтруем пациентов по наличию NaN в колонке "Дата выписки (убытия в часть)"
    hospitalized_patients = [
        patient for patient in data_rkb 
        if pd.isna(patient.get('Дата выписки (убытия в часть)'))
    ]

    return templates.TemplateResponse("other/on_hospitalization_table.html", {"request": request, "data": hospitalized_patients, "has_violation": False})

@router.get("/generate_report", response_class=FileResponse)
async def generate_report(request: Request, patient_id: int):
    # Считываем данные из файлов
    data_rkb, _ = read_excel(FILE_PATH_RKB)
    
    # Получаем данные о конкретном пациенте
    if patient_id < 0 or patient_id >= len(data_rkb):
        raise HTTPException(status_code=404, detail="Пациент не найден")

    patient = data_rkb[patient_id]

    # Шаблон документа
    template_path = os.path.join(docs_dir, "templates\\Отчёт о нарушении.docx")  # Укажите путь к вашему шаблону документа

    # Генерация документа
    output_path = fill_template(template_path, patient, patient['Фамилия и инициалы'], file_name='Справка о нахождении на госпитализации')

    # Возвращаем файл для скачивания
    return FileResponse(output_path, filename=os.path.basename(output_path), media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@router.get("/generate_admission_notification_rkb", response_class=FileResponse)
async def generate_report(request: Request, patient_id: int):
    # Считываем данные из файлов
    data_rkb, _ = read_excel(FILE_PATH_RKB)
    
    # Получаем данные о конкретном пациенте
    if patient_id < 0 or patient_id >= len(data_rkb):
        raise HTTPException(status_code=404, detail="Пациент не найден")

    patient = data_rkb[patient_id]
    patient['Должность'] = 'Временно исполняющий обязанности начальника'
    patient['Звание должностного лица'] = 'подполковник медицинской службы'
    patient['Имя подписывающего'] = 'Р. Сулейманов'
    if isinstance(patient['Дата рождения'], datetime):
        patient['Дата рождения'] = patient['Дата рождения'].strftime("%d.%m.%Y")
    else:
        patient['Дата рождения'] = patient['Дата рождения']  # или None, если хотите

    # Шаблон документа
    template_path = os.path.join(docs_dir, "templates\\Уведомление о нахождении на госпитализации шаблон.docx")  # Укажите путь к вашему шаблону документа

    # Генерация документа
    output_path = fill_template(template_path, patient, patient['Фамилия и инициалы'], file_name='Уведомление о госпитализации')

    # Возвращаем файл для скачивания
    return FileResponse(output_path, filename=os.path.basename(output_path), media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@router.get("/generate_discharge_notification_rkb", response_class=FileResponse)
async def generate_report(request: Request, patient_id: int):
    # Считываем данные из файлов
    data_rkb, _ = read_excel(FILE_PATH_RKB)
    
    # Получаем данные о конкретном пациенте
    if patient_id < 0 or patient_id >= len(data_rkb):
        raise HTTPException(status_code=404, detail="Пациент не найден")

    patient = data_rkb[patient_id]

    print(patient)
    patient['Должность'] = 'Временно исполняющий обязанности начальника'
    patient['Звание должностного лица'] = 'подполковник медицинской службы'
    patient['Имя подписывающего'] = 'Р. Сулейманов'
    if isinstance(patient['Дата рождения'], datetime):
        patient['Дата рождения'] = patient['Дата рождения'].strftime("%d.%m.%Y")
    else:
        patient['Дата рождения'] = patient['Дата рождения']  # или None, если хотите

    # Шаблон документа
    template_path = os.path.join(docs_dir, "templates\\Уведомление о выписке шаблон.docx")  # Укажите путь к вашему шаблону документа

    # Генерация документа
    output_path = fill_template(template_path, patient, patient['Фамилия и инициалы'], file_name='Уведомление о выписке')

    # Возвращаем файл для скачивания
    return FileResponse(output_path, filename=os.path.basename(output_path), media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@router.get("/generate_admission_notification_gkb", response_class=FileResponse)
async def generate_report(request: Request, patient_id: int):
    # Считываем данные из файлов
    data_rkb, _ = read_excel(FILE_PATH_GKB)
    
    # Получаем данные о конкретном пациенте
    if patient_id < 0 or patient_id >= len(data_rkb):
        raise HTTPException(status_code=404, detail="Пациент не найден")

    patient = data_rkb[patient_id]
    patient['Должность'] = 'Временно исполняющий обязанности начальника'
    patient['Звание должностного лица'] = 'подполковник медицинской службы'
    patient['Имя подписывающего'] = 'Р. Сулейманов'
    if isinstance(patient['Дата рождения'], datetime):
        patient['Дата рождения'] = patient['Дата рождения'].strftime("%d.%m.%Y")
    else:
        patient['Дата рождения'] = patient['Дата рождения']  # или None, если хотите

    # Шаблон документа
    template_path = os.path.join(docs_dir, "templates\\Уведомление о нахождении на госпитализации шаблон.docx")  # Укажите путь к вашему шаблону документа

    # Генерация документа
    output_path = fill_template(template_path, patient, patient['Фамилия и инициалы'], file_name='Уведомление о госпитализации')

    # Возвращаем файл для скачивания
    return FileResponse(output_path, filename=os.path.basename(output_path), media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@router.get("/generate_discharge_notification_gkb", response_class=FileResponse)
async def generate_report(request: Request, patient_id: int):
    # Считываем данные из файлов
    data_rkb, _ = read_excel(FILE_PATH_GKB)
    
    # Получаем данные о конкретном пациенте
    if patient_id < 0 or patient_id >= len(data_rkb):
        raise HTTPException(status_code=404, detail="Пациент не найден")

    patient = data_rkb[patient_id]

    print(patient)
    patient['Должность'] = 'Временно исполняющий обязанности начальника'
    patient['Звание должностного лица'] = 'подполковник медицинской службы'
    patient['Имя подписывающего'] = 'Р. Сулейманов'
    if isinstance(patient['Дата рождения'], datetime):
        patient['Дата рождения'] = patient['Дата рождения'].strftime("%d.%m.%Y")
    else:
        patient['Дата рождения'] = patient['Дата рождения']  # или None, если хотите

    # Шаблон документа
    template_path = os.path.join(docs_dir, "templates\\Уведомление о выписке шаблон.docx")  # Укажите путь к вашему шаблону документа

    # Генерация документа
    output_path = fill_template(template_path, patient, patient['Фамилия и инициалы'], file_name='Уведомление о выписке')

    # Возвращаем файл для скачивания
    return FileResponse(output_path, filename=os.path.basename(output_path), media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@router.get("/generate_admission_notification_gvv", response_class=FileResponse)
async def generate_report(request: Request, patient_id: int):
    # Считываем данные из файлов
    data_rkb, _ = read_excel(FILE_PATH_GVV)
    
    # Получаем данные о конкретном пациенте
    if patient_id < 0 or patient_id >= len(data_rkb):
        raise HTTPException(status_code=404, detail="Пациент не найден")

    patient = data_rkb[patient_id]
    patient['Должность'] = 'Временно исполняющий обязанности начальника'
    patient['Звание должностного лица'] = 'подполковник медицинской службы'
    patient['Имя подписывающего'] = 'Р. Сулейманов'
    if isinstance(patient['Дата рождения'], datetime):
        patient['Дата рождения'] = patient['Дата рождения'].strftime("%d.%m.%Y")
    else:
        patient['Дата рождения'] = patient['Дата рождения']  # или None, если хотите

    # Шаблон документа
    template_path = os.path.join(docs_dir, "templates\\Уведомление о нахождении на госпитализации шаблон.docx")  # Укажите путь к вашему шаблону документа

    # Генерация документа
    output_path = fill_template(template_path, patient, patient['Фамилия и инициалы'], file_name='Уведомление о госпитализации')

    # Возвращаем файл для скачивания
    return FileResponse(output_path, filename=os.path.basename(output_path), media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@router.get("/generate_discharge_notification_gvv", response_class=FileResponse)
async def generate_report(request: Request, patient_id: int):
    # Считываем данные из файлов
    data_rkb, _ = read_excel(FILE_PATH_GVV)
    
    # Получаем данные о конкретном пациенте
    if patient_id < 0 or patient_id >= len(data_rkb):
        raise HTTPException(status_code=404, detail="Пациент не найден")

    patient = data_rkb[patient_id]

    print(patient)
    patient['Должность'] = 'Временно исполняющий обязанности начальника'
    patient['Звание должностного лица'] = 'подполковник медицинской службы'
    patient['Имя подписывающего'] = 'Р. Сулейманов'
    if isinstance(patient['Дата рождения'], datetime):
        patient['Дата рождения'] = patient['Дата рождения'].strftime("%d.%m.%Y")
    else:
        patient['Дата рождения'] = patient['Дата рождения']  # или None, если хотите

    # Шаблон документа
    template_path = os.path.join(docs_dir, "templates\\Уведомление о выписке шаблон.docx")  # Укажите путь к вашему шаблону документа

    # Генерация документа
    output_path = fill_template(template_path, patient, patient['Фамилия и инициалы'], file_name='Уведомление о выписке')

    # Возвращаем файл для скачивания
    return FileResponse(output_path, filename=os.path.basename(output_path), media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


@router.get("/patients", response_class=HTMLResponse)
async def patients(request: Request, db: Session = Depends(get_db)):
    try:
        authorize_request(request, db)  # Проверка авторизации
    except HTTPException as e:
        if e.status_code == 401:
            return templates.TemplateResponse("users/access_denied.html", {"request": request})
        raise
 
    data = []

    # Чтение данных из файлов
    data_rkb, has_violation_rkb = read_excel(FILE_PATH_RKB)
    data_gkb7, has_violation_gkb7 = read_excel(FILE_PATH_GKB)
    data_gvv, has_violation_gkb7 = read_excel(FILE_PATH_GVV)

    # Добавление флага источника данных
    for record in data_rkb:
        record['source'] = 'rkb'
    for record in data_gkb7:
        record['source'] = 'gkb7'
    for record in data_gkb7:
        record['source'] = 'gvv'

    data.extend(data_rkb)
    data.extend(data_gkb7)
    data.extend(data_gvv)

    # Чтение данных из старой базы данных
    patients_old = db.query(old_models.PatientData).all()

    data_old = [{
        '№ П/п': patient.history_number,
        'Воинская часть': patient.military_unit,
        'Военное звание, военнослужащий': patient.military_rank,
        'росгвардия / мобилизованный / контрактиник / Вагнер / родственник': patient.service_basis,
        'Фамилия и инициалы': patient.full_name,
        'Дата рождения': patient.birthday_date,
        'Наименование ВМО (филиал)': 'ФГКУ 354 ВКГ',
        'Дата госпитализации': patient.admission_date,    
        'Диагноз по МКБ': patient.diagnosis,
        'Дата выписки (убытия в часть)': patient.assigned_by,
        'ИСХОД': patient.address,
        'Примечание': patient.nature_of_hospitalization,
    } for patient in patients_old]

    data.extend(data_old)

    # Чтение данных из новой базы данных
    patients_new = (
        db.query(models.PassportData, models.HospitalData)
        .join(models.HospitalData, models.HospitalData.patient_id == models.PassportData.id)
        .order_by(models.PassportData.current_time.desc())
        .all()
    )

    for passport_data, hospital_data in patients_new:

        last_movement = (
            db.query(models.PatientMovement)
            .filter(models.PatientMovement.patient_id == passport_data.id)
            .order_by(models.PatientMovement.event_date.desc())
            .first()
        )
        last_movement_date = last_movement.event_date if last_movement else None

        data.append({
            '№ П/п': passport_data.history_number,
            'Воинская часть': passport_data.military_unit,
            'Военное звание, военнослужащий': passport_data.military_rank,
            'росгвардия / мобилизованный / контрактиник / Вагнер / родственник': passport_data.service_basis,
            'Фамилия и инициалы': passport_data.full_name,
            'Дата рождения': passport_data.birthday_date,
            'Наименование ВМО (филиал)': 'ФГКУ 354 ВКГ новая',
            'Дата госпитализации': passport_data.current_time,    
            'Диагноз по МКБ': hospital_data.final_diagnosis,
            'Дата выписки (убытия в часть)': last_movement_date,
            'ИСХОД': passport_data.branch,
            'Примечание': passport_data.nature_of_hospitalization,

        })

    has_violation = has_violation_rkb or has_violation_gkb7

    return templates.TemplateResponse("other/search_by_name.html", {"request": request, "data": data, "has_violation": has_violation})
