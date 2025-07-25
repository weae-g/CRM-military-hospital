from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from fastapi import Form, UploadFile
import os

from ...model.documents.models import DocumentDB
from ...model.documents.schemas import DocumentCreate, Document
from ...model.database.database import SessionLocal

# Путь к папке с шаблонами
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.abspath(os.path.join(current_dir, "../../templates"))
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse, name="document_list")
def read_documents_page(request: Request):
    """
    Отображает страницу со списком документов.
    """
    return templates.TemplateResponse("documents/documents.html", {"request": request})

@router.get("/add", response_class=HTMLResponse, name="add_document")
def add_document_page(request: Request):
    """
    Страница добавления нового документа.
    """
    return templates.TemplateResponse("documents/add_document.html", {"request": request})

@router.get("/documents", response_model=List[Document])
def get_documents(db: Session = Depends(get_db)):
    """
    Получение списка всех документов.

    :param db: Сессия базы данных.
    :return: Список документов.
    """
    documents = db.query(DocumentDB).all()
    return documents

@router.get("/documents/{doc_id}", response_model=Document)
def get_document(doc_id: int, db: Session = Depends(get_db)):
    """
    Получение документа по идентификатору.

    :param doc_id: Идентификатор документа.
    :param db: Сессия базы данных.
    :return: Документ.
    :raises HTTPException: Если документ не найден.
    """
    document = db.query(DocumentDB).filter(DocumentDB.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return document

@router.post("/documents", response_model=Document)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    """
    Создание нового документа.

    :param doc: Данные документа для создания.
    :param db: Сессия базы данных.
    :return: Созданный документ.
    """
    db_doc = DocumentDB(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.put("/documents/{doc_id}", response_model=Document)
def update_document(doc_id: int, doc: DocumentCreate, db: Session = Depends(get_db)):
    """
    Обновление существующего документа.

    :param doc_id: Идентификатор документа для обновления.
    :param doc: Новые данные для документа.
    :param db: Сессия базы данных.
    :return: Обновленный документ.
    :raises HTTPException: Если документ не найден.
    """
    db_doc = db.query(DocumentDB).filter(DocumentDB.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    for key, value in doc.dict().items():
        setattr(db_doc, key, value)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.delete("/documents/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """
    Удаление документа по идентификатору.

    :param doc_id: Идентификатор документа для удаления.
    :param db: Сессия базы данных.
    :return: Сообщение об успешном удалении.
    :raises HTTPException: Если документ не найден.
    """
    db_doc = db.query(DocumentDB).filter(DocumentDB.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    db.delete(db_doc)
    db.commit()
    return {"message": "Документ удален"}

@router.post("/documents/save", response_class=HTMLResponse, name="save_document")
async def save_document(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = None,
    document_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    # Определение пути к директории для хранения файлов
    upload_dir = 'static/docs/at_story'
    os.makedirs(upload_dir, exist_ok=True)  # Создание директории, если она не существует

    if document_id:
        # Обновление существующего документа
        db_doc = db.query(DocumentDB).filter(DocumentDB.id == document_id).first()
        if not db_doc:
            raise HTTPException(status_code=404, detail="Документ не найден")

        db_doc.title = title
        db_doc.description = description
        if file:
            file_location = os.path.join(upload_dir, file.filename)
            with open(file_location, "wb") as f:
                f.write(file.file.read())
            db_doc.file_path = file_location

        db.commit()
        db.refresh(db_doc)
    else:
        # Создание нового документа
        file_location = None
        if file:
            file_location = os.path.join(upload_dir, file.filename)
            with open(file_location, "wb") as f:
                f.write(file.file.read())

        new_doc = DocumentDB(title=title, description=description, file_path=file_location)
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

    return RedirectResponse(url='/document', status_code=302)