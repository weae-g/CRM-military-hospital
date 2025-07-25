from fastapi import FastAPI, Request, APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import os

from ...model.settings.models import Document
from ...model.settings.schemas import DocumentCreate
from ...model.database.database import SessionLocal
from .._utils.documents_utils import templates

router = APIRouter()

def get_db():
    """
    Функция-генератор для создания и управления сеансами базы данных.

    Используется в качестве зависимости в маршрутах для получения сеанса базы данных.

    Yields:
        Session: Сеанс базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """
    Отображение главной страницы настроек.

    Этот эндпоинт возвращает HTML-шаблон главной страницы настроек приложения.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: HTML-страница с главной страницей настроек.
    """
    return templates.TemplateResponse("settings/index.html", {"request": request})

@router.get("/api/documents")
def get_documents(db: Session = Depends(get_db)):
    """
    Получение списка всех документов.

    Этот эндпоинт возвращает список всех документов, хранящихся в базе данных.

    Args:
        db (Session, optional): Сеанс базы данных. По умолчанию используется зависимость `get_db`.

    Returns:
        List[Document]: Список всех документов.
    """
    documents = db.query(Document).all()
    return documents

@router.get("/api/documents/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)):
    """
    Получение документа по его идентификатору.

    Этот эндпоинт возвращает документ с указанным идентификатором, если он существует.
    В противном случае возвращает ошибку 404.

    Args:
        doc_id (int): Идентификатор документа.
        db (Session, optional): Сеанс базы данных. По умолчанию используется зависимость `get_db`.

    Returns:
        Document: Документ с указанным идентификатором.

    Raises:
        HTTPException: Если документ не найден (статус 404).
    """
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.post("/api/documents", response_model=DocumentCreate)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    """
    Создание нового документа.

    Этот эндпоинт создает новый документ в базе данных на основе предоставленных данных.

    Args:
        doc (DocumentCreate): Данные для создания нового документа.
        db (Session, optional): Сеанс базы данных. По умолчанию используется зависимость `get_db`.

    Returns:
        DocumentCreate: Созданный документ.
    """
    db_doc = Document(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.put("/api/documents/{doc_id}")
def update_document(doc_id: int, doc: DocumentCreate, db: Session = Depends(get_db)):
    """
    Обновление существующего документа по его идентификатору.

    Этот эндпоинт обновляет документ с указанным идентификатором на основе предоставленных данных.
    В противном случае возвращает ошибку 404.

    Args:
        doc_id (int): Идентификатор документа для обновления.
        doc (DocumentCreate): Новые данные для документа.
        db (Session, optional): Сеанс базы данных. По умолчанию используется зависимость `get_db`.

    Returns:
        Document: Обновленный документ.

    Raises:
        HTTPException: Если документ не найден (статус 404).
    """
    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")
    for key, value in doc.dict().items():
        setattr(db_doc, key, value)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.delete("/api/documents/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """
    Удаление документа по его идентификатору.

    Этот эндпоинт удаляет документ с указанным идентификатором из базы данных.
    В противном случае возвращает ошибку 404.

    Args:
        doc_id (int): Идентификатор документа для удаления.
        db (Session, optional): Сеанс базы данных. По умолчанию используется зависимость `get_db`.

    Returns:
        dict: Сообщение об успешном удалении документа.

    Raises:
        HTTPException: Если документ не найден (статус 404).
    """
    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(db_doc)
    db.commit()
    return {"message": "Document deleted"}
