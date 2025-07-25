from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os

router = APIRouter()

# Получаем путь к директории
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.abspath(os.path.join(current_dir, "../templates"))
docs_dir = os.path.abspath(os.path.join(current_dir, "../static/docs/Госпиталь справочник 1.docx"))
# Инициализируем Jinja2Templates
templates = Jinja2Templates(directory=templates_dir)

@router.get("/archive", response_class=HTMLResponse)
async def read_documents(request: Request):
    # Допустим, у вас есть некоторые данные, которые хотите передать в шаблон
    documents = [
        {"name": "Документ 1", "description": "Краткое описание документа 1, содержащее основную информацию о содержимом.", "link": "document1.pdf"},
        {"name": "Документ 2", "description": "Краткое описание документа 2, для более детального понимания его содержания.", "link": "document2.pdf"},
        {"name": "Документ 3", "description": "Краткое описание документа 3, указывающее на важные аспекты и назначение документа.", "link": "document3.pdf"}
    ]
    return templates.TemplateResponse("documents.html", {"request": request, "documents": documents})
