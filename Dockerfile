# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .
COPY package.json .
COPY package-lock.json* .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Устанавливаем дополнительные зависимости для production
RUN pip install --no-cache-dir uvicorn[standard] gunicorn python-dotenv

# Копируем весь проект
COPY website/ /app/website/

# Создаем директорию для логов
RUN mkdir -p /app/website/app/logs

# Создаем временную директорию для приложения
RUN mkdir -p /app/temp && chmod 777 /app/temp

# Создаем пользователя без root прав
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Открываем порт
EXPOSE 8000

# Запускаем приложение с помощью uvicorn
CMD ["uvicorn", "website.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
