from fastapi import APIRouter, Request, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from ...model.user.models import UserDB
from ...model.user.schemas import UserCreate, User
from . import crud   
from ...model.user.auth import authorize_request
import os

router = APIRouter()

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.abspath(os.path.join(current_dir, "../../templates"))
templates = Jinja2Templates(directory=templates_dir)


@router.get("/", response_class=HTMLResponse, name="user_list")
async def read_users_page(request: Request, db: Session = Depends(crud.get_db)):
    """
    Извлекает и рендерит список пользователей в шаблоне user_list.html.
    
    Аргументы:
        request: HTTP запрос.
        db: Зависимость сессии базы данных.

    Возвращает:
        HTMLResponse: Отрендеренная HTML страница со списком пользователей.
    """
    try:
        authorize_request(request, db)  # Проверка авторизации
    except HTTPException as e:
        if e.status_code == 401:
            return templates.TemplateResponse("users/access_denied.html", {"request": request})
        raise
    users = crud.get_users(db)
    return templates.TemplateResponse("users/user_list.html", {"request": request, "users": users})


@router.get("/delete_user", response_class=HTMLResponse, name="delete_user")
def delete_user(id: int, db: Session = Depends(crud.get_db)):
    """
    Deletes a user identified by the given ID from the database.
    
    Args:
        id: The ID of the user to be deleted.
        db: Database session dependency.

    Returns:
        RedirectResponse: Redirects to the user list page after deletion.
        
    Raises:
        HTTPException: If the user with the specified ID does not exist.
    """
    user_to_delete = db.query(UserDB).filter(UserDB.id == id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")
    return RedirectResponse(url="/users", status_code=302)


@router.post("/add_user", response_model=User)
def create_user(
    username: str = Form(...),
    password: str = Form(...),
    ip_addresses: str = Form(None),
    full_name: str = Form(...),
    cabinet: str = Form(None),
    role: str = Form(...),
    db: Session = Depends(crud.get_db)
):
    """
    Creates a new user with the provided data and saves it to the database.
    
    Args:
        username: The username of the new user.
        password: The password for the new user.
        ip_addresses: Optional IP addresses associated with the new user.
        full_name: The full name of the new user.
        cabinet: Optional cabinet information for the new user.
        role: The role assigned to the new user.
        db: Database session dependency.

    Returns:
        RedirectResponse: Redirects to the user list page after creating the user.
    """
    user_data = UserCreate(
        username=username,
        password=password,
        ip_addresses=ip_addresses,
        full_name=full_name,
        cabinet=cabinet,
        role=role
    )
    db_user = crud.create_user(db, user_data)
    return RedirectResponse(url="/users", status_code=302)
