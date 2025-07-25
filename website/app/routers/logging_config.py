import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_directory: str = "logs", log_filename: str = "app.log"):
    """
    Настройка системы логирования для приложения.

    Эта функция конфигурирует логирование с записью логов в файл и выводом в консоль. Она создает каталог для логов, 
    если он не существует, и настраивает логгер для записи логов с помощью ротации файлов и форматирования сообщений.

    Args:
        log_directory (str, optional): Директория для хранения лог-файлов. По умолчанию "logs".
        log_filename (str, optional): Имя лог-файла. По умолчанию "app.log".

    Returns:
        None

    Example:
        >>> setup_logging()
    """
    # Создание директории для логов, если она не существует
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file_path = os.path.join(log_directory, log_filename)

    # Создаем логгер
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.DEBUG)  # Установка уровня логгирования

    # Формат логирования
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'  # Формат дат
    )

    # Обработчик логирования в файл с ротацией
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1024*1024*5, backupCount=10)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Обработчик логирования в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
