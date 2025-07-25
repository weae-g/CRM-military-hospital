from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import logging
import os

logger = logging.getLogger(__name__)
document_clinic_router = APIRouter()

current_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.abspath(os.path.join(current_dir, "../static/docs"))
img_dir = os.path.abspath(os.path.join(current_dir, "../static/img"))
js_dir = os.path.abspath(os.path.join(current_dir, "../static/js"))
css_dir = os.path.abspath(os.path.join(current_dir, "../static/css"))
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../templates"))
templates = Jinja2Templates(directory=frontend_dir)


@document_clinic_router.get("/documents", response_class=HTMLResponse)
async def read_root(request: Request):
    pdf_url =  os.path.join(docs_dir , "clinic_sample/VШаблон осмотра ЛОР-врача.pdf")
    return templates.TemplateResponse("view_html/documents.html", {"request": request, "pdf_url": pdf_url})

