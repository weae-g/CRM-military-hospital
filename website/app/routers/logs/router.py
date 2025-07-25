import os
from collections import defaultdict
from datetime import datetime
from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse

# Директория для хранения лог-файлов
log_directory = 'app\\logs'
# Путь к текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))
# Инициализация шаблонов Jinja2
templates = Jinja2Templates(directory=os.path.abspath(os.path.join(current_dir, "../../templates")))

router = APIRouter()

# Путь к файлу лога
log_file_path = os.path.join(log_directory, "app.log")

@router.get("/log")
async def get_log():
    """
    Получение содержимого лог-файла в виде текста.

    Этот эндпоинт читает содержимое лог-файла `app.log`, если файл существует, 
    и возвращает его в виде текстового ответа. Если файл не найден, возвращается
    сообщение об ошибке.

    Returns:
        PlainTextResponse: Содержимое лог-файла или сообщение об ошибке.
    """
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8', errors='replace') as log_file:
            content = log_file.read()
        return PlainTextResponse(content)
    else:
        return PlainTextResponse("Log file not found")

@router.get("/view_log")
async def view_log(request: Request):
    """
    Отображение веб-страницы для просмотра логов.

    Этот эндпоинт рендерит HTML-шаблон для отображения страницы логов. Шаблон 
    загружается из директории `templates`, и в контекст шаблона передается 
    объект `request`.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница для просмотра логов.
    """
    return templates.TemplateResponse("logs/index.html", {"request": request})
