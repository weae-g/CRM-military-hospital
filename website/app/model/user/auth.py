# auth.py

from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from .models import UserDB
from .schemas import User

# Define allowed IP addresses
ALLOWED_IPS = [
    "127.0.0.1", "192.168.15.205", "192.168.15.203", 
    "192.168.15.228", "192.168.15.115"
]

ALLOWED_IPS_VVK = ALLOWED_IPS + ["192.168.15.76"]

def check_ip(request: Request):
    """
    Checks if the client's IP address is in the list of allowed IP addresses.
    
    Args:
        request: The HTTP request object.
    
    Raises:
        HTTPException: If the client's IP address is not allowed.
    """
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail="Доступ запрещен.")

def check_ip_vvk(request: Request):
    """
    Checks if the client's IP address is in the list of allowed IP addresses 
    for VVK and medical certificate changes.
    
    Args:
        request: The HTTP request object.
    
    Raises:
        HTTPException: If the client's IP address is not allowed.
    """
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS_VVK:
        raise HTTPException(status_code=403, detail="Доступ запрещен.")

def authenticate_user(username: str, password: str, db: Session) -> User:
    """
    Authenticates a user based on username and password.
    
    Args:
        username: The username of the user.
        password: The password of the user.
        db: The database session.
    
    Returns:
        User: The authenticated user.
    
    Raises:
        HTTPException: If the user is not found or the password is incorrect.
    """
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None or user.password != password:
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль.")


def authorize_request(request: Request, db: Session) -> User:
    ip = request.client.host
    user = db.query(UserDB).filter(UserDB.ip_addresses.contains(ip)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не имеет соответствующего доступа.")
    
    return None
    