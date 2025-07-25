"""
Этот скрипт загружает переменные окружения из файла .env, инициализирует подключение к базе данных, 
создаёт фабрику сессий и базовый класс для декларативных моделей SQLAlchemy.
"""


import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Получить текущий рабочий каталог
current_dir = os.getcwd()

# Сконструировать путь к файлу .env, используя os.path.join
env_path = os.path.join(current_dir, "app", ".env")

# Загрузить переменные окружения из файла .env
load_dotenv(dotenv_path=env_path)

# Получить URL базы данных из переменных окружения
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Проверить, что DATABASE_URL загружен правильно
if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("DATABASE_URL не установлен в файле .env")

# Создать движок SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создать фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для декларативных моделей
Base = declarative_base()
