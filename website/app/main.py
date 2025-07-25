from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routers import document, pacient_passport, main_page, directory
from .routers.clinic_router import clinic
from .routers.vvk import vvk_router
from .routers.document_clinic import router
from .routers.other import other_router
from .routers.settings import settings
from .routers.logs import router as logs_router
from .routers.documents import router as document_router
from .routers.user import router as user_router
from .routers.vpd import router as vpd_router
from datetime import datetime
from logging.handlers import RotatingFileHandler
import logging
import os

app = FastAPI()

# Папка для логов
log_directory = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_directory, exist_ok=True)  # Создать папку, если она еще не существует

# Настройка логгера
log_file_path = os.path.join(log_directory, "app.log")
logger = logging.getLogger("my_app_logger")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent propagation to avoid duplicate logs
# Добавляем вращающийся обработчик файлов
handler = RotatingFileHandler(log_file_path, maxBytes=10000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_client_ip(request: Request) -> str:
    """
    Извлекает IP-адрес клиента из заголовка "X-Forwarded-For" или из адреса клиента, если заголовок отсутствует.

    Параметры:
    request (Request): Объект запроса FastAPI.

    Возвращает:
    str: IP-адрес клиента.
    """
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host
    return ip

def log_request_data(request: Request):
    """
    Логирует данные запроса, включая текущее время, IP-адрес клиента, метод HTTP и путь запроса.

    Параметры:
    request (Request): Объект запроса FastAPI.
    """
    current_time = datetime.now().strftime('%d.%m.%Y в %H:%M')
    logger.info(f"Date and Time: {current_time}, IP: {get_client_ip(request)}, Method: {request.method}, Path: {request.url.path}")

@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    """
    Middleware для логирования данных запроса перед его обработкой.

    Параметры:
    request (Request): Объект запроса FastAPI.
    call_next (Callable): Функция для вызова следующего middleware или обработки запроса.

    Возвращает:
    Response: Ответ от обработки запроса.
    """
    try:
        ip = get_client_ip(request)
        # Логируем запрос только если путь не заканчивается на 'favicon.ico'
        if not request.url.path.endswith('favicon.ico'):
            log_request_data(request)
    except Exception as e:
        logger.error(f"Failed to log request: {e}")
    response = await call_next(request)
    return response


docs_directory = Path(__file__).parent / "static/docs"
# Проверяем, существует ли директория
if not docs_directory.exists():
    raise RuntimeError(f"Directory '{docs_directory}' does not exist")

img_directory = Path(__file__).parent / "static/img"
# Проверяем, существует ли директория
if not img_directory.exists():
    raise RuntimeError(f"Directory '{img_directory}' does not exist")

style_directory = Path(__file__).parent / "static/css"
# Проверяем, существует ли директория
if not style_directory.exists():
    raise RuntimeError(f"Directory '{style_directory}' does not exist")

js_directory = Path(__file__).parent / "static/js"
# Проверяем, существует ли директория
if not js_directory.exists():
    raise RuntimeError(f"Directory '{js_directory}' does not exist")

base_directory = Path(__file__).parent / "templates/base"
# Проверяем, существует ли директория
if not base_directory.exists():
    raise RuntimeError(f"Directory '{base_directory}' does not exist")

# Подключаем директорию для обслуживания статических файлов
#app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/docs", StaticFiles(directory=docs_directory), name="docs")
app.mount("/img", StaticFiles(directory=img_directory), name="img")
app.mount("/css", StaticFiles(directory=style_directory), name="css")
app.mount("/js", StaticFiles(directory=js_directory), name="js")
app.mount("/base", StaticFiles(directory=base_directory), name="base")

app.include_router(main_page.router)
app.include_router(vpd_router.router, prefix="/vpd")
app.include_router(user_router.router, prefix="/users")
app.include_router(document_router.router, prefix="/document")
app.include_router(logs_router.router, prefix="/logs")
app.include_router(settings.router, prefix="/settings")
app.include_router(other_router.router, prefix="/otx")
app.include_router(clinic.router, prefix="/clinic")
app.include_router(pacient_passport.router, prefix="/pacients")
app.include_router(directory.router, prefix="/directory")
#app.include_router(document.router, prefix="/document")
app.include_router(vvk_router.router, prefix="/vvk")
app.include_router(router.document_clinic_router, prefix="/document_clinic")

from fastapi.templating import Jinja2Templates

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.abspath(os.path.join(current_dir, "templates"))
templates = Jinja2Templates(directory=templates_dir)

from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Обработчик исключений HTTP для отображения страницы ошибки доступа.
    
    Аргументы:
        request: HTTP запрос.
        exc: Исключение HTTPException.
    
    Возвращает:
        HTMLResponse: Отрендеренная HTML страница ошибки.
    """
    if exc.status_code == 401:
        return templates.TemplateResponse("users/access_denied.html", {"request": request})
    # Обработка других исключений
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )




