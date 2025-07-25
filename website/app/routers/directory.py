from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ._utils.documents_utils import templates
from mammoth import convert_to_html
import os

from dotenv import load_dotenv

# Загрузить переменные окружения из файла .env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), "app", ".env"))

FILE_SAXONY = os.getenv("file_saxony")


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request): 
    with open(FILE_SAXONY, "rb") as file:
        result = convert_to_html(file)
        html = result.value

    template = "directory.html"
    return templates.TemplateResponse(template, {"request": request, "word_content": html})
