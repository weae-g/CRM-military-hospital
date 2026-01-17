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

# Создаем пользователя без root прав
RUN useradd -m -u 1000 appuser

# Создаем директории с правильными разрешениями
RUN mkdir -p /app/website/app/logs && \
    mkdir -p /app/temp && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chmod -R 777 /app/website/app/logs && \
    chmod -R 777 /app/temp

USER appuser

# Открываем порт
EXPOSE 8000

# Запускаем приложение с помощью uvicorn
CMD ["uvicorn", "website.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
