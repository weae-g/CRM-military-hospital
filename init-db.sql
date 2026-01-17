-- Инициализация базы данных
-- Этот скрипт выполняется при первом запуске PostgreSQL контейнера

-- Создание базы данных (если нужно)
-- CREATE DATABASE Patients;

-- Подключение к базе данных
\c Patients;

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Здесь можно добавить начальные таблицы или данные
-- Пример:
-- CREATE TABLE IF NOT EXISTS example_table (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Вывод информации
SELECT 'Database initialized successfully!' AS message;
