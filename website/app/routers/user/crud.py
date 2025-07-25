from sqlalchemy.orm import Session
from ...model.user.models import UserDB
from ...model.user.schemas import UserCreate, User

def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Получает список пользователей из базы данных с возможностью пропуска и ограничения количества.

    :param db: Экземпляр сессии SQLAlchemy.
    :param skip: Количество пользователей, которое нужно пропустить. По умолчанию 0.
    :param limit: Максимальное количество пользователей для получения. По умолчанию 10.
    :return: Список пользователей.
    """
    return db.query(UserDB).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """
    Создает нового пользователя в базе данных.

    :param db: Экземпляр сессии SQLAlchemy.
    :param user: Данные пользователя, которые нужно создать, переданные в виде схемы UserCreate.
    :return: Созданный пользователь.
    """
    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    """
    Получает пользователя по его идентификатору.

    :param db: Экземпляр сессии SQLAlchemy.
    :param user_id: Идентификатор пользователя.
    :return: Найденный пользователь или None, если пользователь не найден.
    """
    return db.query(UserDB).filter(UserDB.id == user_id).first()

def delete_user(db: Session, user_id: int):
    """
    Удаляет пользователя по его идентификатору.

    :param db: Экземпляр сессии SQLAlchemy.
    :param user_id: Идентификатор пользователя.
    :return: True, если пользователь был успешно удален, иначе False.
    """
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def get_db():
    """
    Создает и управляет сессией базы данных.

    Используется в качестве генератора, чтобы обеспечить корректное закрытие сессии после использования.

    :yield: Экземпляр сессии SQLAlchemy.
    """
    from ...model.database.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
