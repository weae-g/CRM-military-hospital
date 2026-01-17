# Руководство по развертыванию CRM Hospital на Linux сервере

## Требования

- Linux сервер (Ubuntu 20.04/22.04, Debian 11/12, CentOS 7/8 или аналогичные)
- Минимум 2GB RAM, 2 CPU cores
- Минимум 20GB свободного места на диске
- Статический IP адрес
- Root или sudo доступ

## Быстрый старт (Автоматическая установка)

### Шаг 1: Подключитесь к серверу

```bash
ssh user@your-server-ip
```

### Шаг 2: Установка Docker (если не установлен)

```bash
# Обновляем систему
sudo apt-get update && sudo apt-get upgrade -y

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавляем текущего пользователя в группу docker
sudo usermod -aG docker $USER

# Устанавливаем Docker Compose
sudo apt-get install docker-compose-plugin -y

# Перезагружаем сессию или выходим и заходим снова
newgrp docker

# Проверяем установку
docker --version
docker compose version
```

### Шаг 2.5: Установка PostgreSQL клиента (опционально, но рекомендуется)

PostgreSQL клиент нужен для управления базой данных, создания резервных копий и диагностики.

```bash
# Для Ubuntu/Debian
sudo apt-get install postgresql-client -y

# Для CentOS/RHEL
sudo yum install postgresql -y

# Проверяем установку
psql --version
```

**Примечание**: Даже если вы используете PostgreSQL в Docker контейнере, клиент на хосте полезен для:

- Прямого подключения к базе данных
- Создания резервных копий
- Выполнения SQL запросов
- Диагностики проблем

### Шаг 3: Загрузите проект на сервер

**Вариант A: Через Git (рекомендуется)**

```bash
# Клонируем репозиторий
git clone https://github.com/weae-g/CRM-military-hospital.git
cd CRM-military-hospital
```

**Вариант B: Через SCP/SFTP**

```bash
# На вашем локальном компьютере выполните:
scp -r c:\Users\weae\Desktop\weae\CRM-military-hospital user@your-server-ip:/home/user/

# Затем на сервере:
cd /home/user/CRM-military-hospital
```

### Шаг 4: Настройте конфигурацию

```bash
# Копируем пример конфигурации
cp .env.production .env

# Редактируем конфигурацию
nano .env
```

**Важно! Измените следующие параметры:**

```env
# Измените пароль базы данных!
POSTGRES_PASSWORD=ваш_безопасный_пароль

# Настройте порты (если нужно)
NGINX_PORT=80
WEB_PORT=8000

# Обновите DATABASE_URL с новым паролем
DATABASE_URL=postgresql://postgres:ваш_безопасный_пароль@db:5432/Patients
```

Также обновите файл `website/app/.env`:

```bash
nano website/app/.env
```

```env
DATABASE_URL=postgresql://postgres:ваш_безопасный_пароль@db:5432/Patients
```

### Шаг 5: Запустите приложение

```bash
# Делаем скрипт исполняемым
chmod +x deploy.sh

# Запускаем приложение
./deploy.sh start

# Дождитесь завершения (может занять 1-2 минуты)
```

**Важно!** Если видите ошибку 502 Bad Gateway сразу после запуска:

```bash
# Подождите 30-60 секунд для полной инициализации
sleep 30

# Проверьте логи web контейнера
docker-compose logs web

# Если есть ошибки подключения к БД, проверьте файл website/app/.env
nano website/app/.env

# DATABASE_URL должен быть:
# DATABASE_URL=postgresql://postgres:ваш_пароль@db:5432/Patients
# Важно: используйте @db, а не @localhost!

# После изменения .env перезапустите:
docker-compose restart web
```

### Шаг 6: Проверьте работу

После успешного запуска приложение будет доступно:

- **Веб-интерфейс**: `http://your-server-ip:80`
- **API документация**: `http://your-server-ip:80/docs`
- **Альтернативная документация**: `http://your-server-ip:80/redoc`

## Команды управления

```bash
# Запуск приложения
./deploy.sh start

# Остановка приложения
./deploy.sh stop

# Перезапуск приложения
./deploy.sh restart

# Просмотр логов
./deploy.sh logs

# Обновление приложения
./deploy.sh update

# Статус сервисов
./deploy.sh status

# Резервное копирование БД
./deploy.sh backup
```

## Настройка Nginx и портов

### Изменение порта приложения

Отредактируйте `.env` файл:

```env
NGINX_PORT=8080  # Изменить порт с 80 на 8080
```

Перезапустите:

```bash
./deploy.sh restart
```

### Доступ напрямую к FastAPI (без Nginx)

Если хотите использовать только FastAPI без Nginx:

```bash
# Отредактируйте docker-compose.yml и закомментируйте секцию nginx
nano docker-compose.yml

# Приложение будет доступно на порту WEB_PORT (по умолчанию 8000)
```

## Настройка SSL/HTTPS (опционально)

### Вариант 1: С использованием Let's Encrypt (рекомендуется)

```bash
# Установите certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Получите SSL сертификат (замените на ваш домен)
sudo certbot certonly --standalone -d yourdomain.com

# Сертификаты будут в /etc/letsencrypt/live/yourdomain.com/

# Обновите docker-compose.yml для монтирования сертификатов:
nano docker-compose.yml
```

Добавьте в секцию nginx volumes:

```yaml
volumes:
  - ./nginx.conf:/etc/nginx/nginx.conf:ro
  - ./website/app/static:/var/www/static:ro
  - /etc/letsencrypt:/etc/letsencrypt:ro # Добавить эту строку
```

Раскомментируйте HTTPS секцию в `nginx.conf` и обновите пути к сертификатам.

### Вариант 2: Самоподписанный сертификат (для тестирования)

```bash
# Создайте директорию для сертификатов
mkdir -p ssl

# Создайте самоподписанный сертификат
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem

# Обновите docker-compose.yml и nginx.conf соответственно
```

## Работа с базой данных

### Подключение к базе данных

**Вариант 1: Через контейнер (всегда работает)**

```bash
# Подключение к БД внутри контейнера
docker-compose exec db psql -U postgres -d Patients

# Выполнение SQL команды
docker-compose exec db psql -U postgres -d Patients -c "SELECT version();"

# Список всех таблиц
docker-compose exec db psql -U postgres -d Patients -c "\dt"
```

**Вариант 2: С хост-машины (если установлен psql клиент)**

```bash
# ВАЖНО! Нужно указывать -h localhost, иначе psql попытается подключиться через Unix socket

# Узнайте пароль из .env файла
cat .env | grep POSTGRES_PASSWORD

# Подключитесь к БД (замените пароль)
PGPASSWORD=ваш_пароль psql -h localhost -U postgres -d Patients

# Или экспортируйте пароль один раз для удобства
export PGPASSWORD=$(cat .env | grep POSTGRES_PASSWORD | cut -d'=' -f2)
psql -h localhost -U postgres -d Patients

# Если порт изменен в .env (не 5432), укажите его:
psql -h localhost -p 5432 -U postgres -d Patients
```

**Частая ошибка:**

```
psql: error: could not connect to server: No such file or directory
        Is the server running locally and accepting
        connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?
```

**Решение:** Всегда указывайте `-h localhost` при подключении к PostgreSQL в Docker!

### Миграции базы данных

Если используете Alembic для миграций:

```bash
# Войдите в контейнер приложения
docker-compose exec web bash

# Выполните миграции
cd website
alembic upgrade head

# Выйдите из контейнера
exit
```

### Полезные SQL команды

```bash
# ВАЖНО: Для всех команд с хоста добавляйте -h localhost

# Размер базы данных (через контейнер)
docker-compose exec db psql -U postgres -d Patients -c "SELECT pg_size_pretty(pg_database_size('Patients'));"

# Размер базы данных (с хоста)
export PGPASSWORD=$(cat .env | grep POSTGRES_PASSWORD | cut -d'=' -f2)
psql -h localhost -U postgres -d Patients -c "SELECT pg_size_pretty(pg_database_size('Patients'));"

# Список всех таблиц с размерами
docker-compose exec db psql -U postgres -d Patients -c "
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"

# Количество записей в таблице (замените table_name)
docker-compose exec db psql -U postgres -d Patients -c "SELECT COUNT(*) FROM table_name;"

# Список активных подключений
docker-compose exec db psql -U postgres -d Patients -c "SELECT * FROM pg_stat_activity WHERE datname = 'Patients';"
```

### Создание алиаса для удобства

Чтобы не вводить пароль и параметры каждый раз, создайте алиас:

```bash (через контейнер)
docker-compose exec db pg_dump -U postgres Patients > backup.sql

# Ручное резервное копирование (с хоста, если установлен psql)
export PGPASSWORD=$(cat .env | grep POSTGRES_PASSWORD | cut -d'=' -f2)
pg_dump -h localhost -U postgres Patients > backup_$(date +%Y%m%d_%H%M%S).sql

# Резервное копирование в сжатом виде
docker-compose exec db pg_dump -U postgres Patients | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Резервное копирование всего проекта
tar -czf crm-backup-$(date +%Y%m%d).tar.gz \
  --exclude='website/Lib' \
  --exclude='website/Include' \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  .
```

### Восстановление из резервной копии

```bash
# Восстановление базы данных (из обычного backup)
cat backup.sql | docker-compose exec -T db psql -U postgres Patients

# Восстановление из сжатого backup
gunzip -c backup.sql.gz | docker-compose exec -T db psql -U postgres Patients

# Восстановление с хоста (если установлен psql)
export PGPASSWORD=$(cat .env | grep POSTGRES_PASSWORD | cut -d'=' -f2)
psql -h localhost -U postgres Patients < backup.sql

# Восстановление с пересозданием базы
docker-compose exec db psql -U postgres -c "DROP DATABASE IF EXISTS Patients;"
docker-compose exec db psql -U postgres -c "CREATE DATABASE Patients;"це (замените table_name)
docker-compose exec db psql -U postgres -d Patients -c "SELECT COUNT(*) FROM table_name;"
```

## Мониторинг и обслуживание

### Просмотр логов

```bash
# Все логи
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx

# Логи приложения на диске
tail -f website/app/logs/app.log
```

### Проверка использования ресурсов

```bash
# Статистика контейнеров
docker stats

# Использование дискового пространства
docker system df
```

### Резервное копирование

```bash
# Автоматическое резервное копирование БД
./deploy.sh backup

# Ручное резервное копирование
docker-compose exec db pg_dump -U postgres Patients > backup.sql

# Резервное копирование всего проекта
tar -czf crm-backup-$(date +%Y%m%d).tar.gz \
  --exclude='website/Lib' \
  --exclude='website/Include' \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  .
```

### Восстановление из резервной копии

```bash
# Восстановление базы данных
cat backup.sql | docker-compose exec -T db psql -U postgres Patients
```

## Автоматический запуск при перезагрузке сервера

Контейнеры настроены с `restart: unless-stopped`, поэтому они автоматически запустятся после перезагрузки сервера.

Если нужно отключить автозапуск:

```bash
docker-compose down
docker update --restart=no $(docker ps -a -q)
```

## Обновление приложения

```bash
# Если используете Git
git pull
./deploy.sh update

# Или вручную
./deploy.sh stop
# Загрузите новые файлы
./deploy.sh start
```

## Настройка firewall

```bash
# Разрешаем HTTP трафик
sudo ufw allow 80/tcp

# Разрешаем HTTPS трафик
sudo ufw allow 443/tcp

# Если нужен прямой доступ к PostgreSQL (не рекомендуется для production)
# sudo ufw allow 5432/tcp

# Включаем firewall
sudo ufw enable

# Проверяем статус
sudo ufw status
```

## Производительность и оптимизация

### Увеличение количества worker'ов

Отредактируйте `Dockerfile`:

```dockerfile
# Измените количество workers (рекомендуется: 2 * CPU_cores + 1)
CMD ["uvicorn", "website.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]
```

### Настройка PostgreSQL

Создайте файл `postgresql.conf` для оптимизации:

```bash
# Добавьте в docker-compose.yml под volumes для db:
- ./postgresql.conf:/etc/postgresql/postgresql.conf
```

## Устранение неполадок

### Ошибка 502 Bad Gateway (nginx)

Это самая частая проблема! Nginx запущен, но не может связаться с FastAPI приложением.

**Шаг 1: Проверьте статус всех контейнеров**

```bash
docker-compose ps

# Все три контейнера должны быть в статусе "Up"
# NAME                  COMMAND                  SERVICE   STATUS    PORTS
# crm_hospital_db       "docker-entrypoint.s…"   db        Up        0.0.0.0:5432->5432/tcp
# crm_hospital_web      "uvicorn website.app…"   web       Up        0.0.0.0:8000->8000/tcp
# crm_hospital_nginx    "/docker-entrypoint.…"   nginx     Up        0.0.0.0:80->80/tcp
```

**Шаг 2: Проверьте логи web контейнера (FastAPI)**

```bash
# Смотрим логи приложения
docker-compose logs web

# Смотрим логи в реальном времени
docker-compose logs -f web

# Ищем ошибки
docker-compose logs web | grep -i error
docker-compose logs web | grep -i exception
```

**Типичные ошибки в логах web:**

1. **Ошибка подключения к базе данных:**

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Решение:** Проверьте DATABASE_URL в файле `website/app/.env`:

```bash
nano website/app/.env

# Должно быть:
DATABASE_URL=postgresql://postgres:ваш_пароль@db:5432/Patients

# Важно: используйте @db, а не @localhost в Docker окружении!
```

2. **Модуль не найден:**

```
ModuleNotFoundError: No module named 'fastapi'
```

**Решение:** Пересоберите образ:

```bash
docker-compose down
docker-compose build --no-cache web
docker-compose up -d
```

3. **Ошибка в Python коде:**
   Проверьте логи на наличие трассировки ошибок и исправьте код.

**Шаг 3: Проверьте доступность FastAPI напрямую**

```bash
# Проверьте, отвечает ли FastAPI на порту 8000
curl http://localhost:8000

# Если не отвечает, web контейнер не работает правильно
# Если отвечает, проблема в nginx конфигурации
```

**Шаг 4: Проверьте сеть между контейнерами**

```bash
# Войдите в nginx контейнер
docker-compose exec nginx sh

# Попробуйте достучаться до web
wget -O- http://web:8000
# или
ping web

# Выход из контейнера
exit
```

**Шаг 5: Перезапуск сервисов**

```bash
# Перезапустите web контейнер
docker-compose restart web

# Подождите 5-10 секунд и проверьте снова
sleep 5
docker-compose logs web

# Если не помогло, перезапустите все
./deploy.sh restart
```

**Шаг 6: Проверка конфигурации**

```bash
# Убедитесь, что .env файл существует в корне проекта
cat .env

# Убедитесь, что website/app/.env существует
cat website/app/.env

# Проверьте, что пароли совпадают в обоих файлах
grep POSTGRES_PASSWORD .env
grep DATABASE_URL website/app/.env
```

### Приложение не запускается

```bash
# Проверьте статус контейнеров
docker-compose ps

# Проверьте логи всех сервисов
docker-compose logs

# Проверьте доступность портов
sudo netstat -tulpn | grep -E ':(80|8000|5432)'

# Проверьте использование ресурсов
docker stats --no-stream
```

### База данных не подключается

**Проблема 1: "No such file or directory" при использовании psql**

```bash
# Ошибка:
# psql: error: could not connect to server: No such file or directory
#         Is the server running locally and accepting
#         connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?

# Решение: Укажите хост явно!
export PGPASSWORD=$(cat .env | grep POSTGRES_PASSWORD | cut -d'=' -f2)
psql -h localhost -U postgres -d Patients

# Без -h localhost psql пытается подключиться через Unix socket,
# но PostgreSQL работает в Docker контейнере на TCP порту
```

**Проблема 2: Контейнер БД не запущен**

```bash
# Проверьте, запущен ли контейнер БД
docker-compose ps db

# Должен показать статус "Up"
# Если статус "Exit", смотрите логи:
docker-compose logs db

# Перезапустите контейнер
docker-compose restart db
```

**Проблема 3: Проверка подключения**

```bash
# Проверьте подключение изнутри контейнера (всегда работает)
docker-compose exec db psql -U postgres -d Patients -c "SELECT 1;"

# Проверьте подключение с хоста (если установлен psql)
export PGPASSWORD=$(cat .env | grep POSTGRES_PASSWORD | cut -d'=' -f2)
psql -h localhost -U postgres -d Patients -c "SELECT 1;"

# Проверьте, что порт PostgreSQL доступен
nc -zv localhost 5432
# или
telnet localhost 5432

# Проверьте переменные окружения в контейнере
docker-compose exec db env | grep POSTGRES
```

### Порт уже занят

```bash
# Найдите процесс, использующий порт
sudo lsof -i :80

# Остановите процесс или измените порт в .env файле
```

## Безопасность

### Рекомендации:

1. **Измените пароль базы данных** в `.env` файле
2. **Используйте HTTPS** в production
3. **Ограничьте доступ к PostgreSQL** порту (не открывайте 5432 наружу)
4. **Регулярно обновляйте** Docker образы: `./deploy.sh update`
5. **Настройте регулярные бэкапы**: добавьте в cron

```bash
# Добавьте в crontab
crontab -e

# Ежедневный бэкап в 2 часа ночи
0 2 * * * cd /path/to/CRM-military-hospital && ./deploy.sh backup
```

## Контакты и поддержка

При возникновении проблем:

1. Проверьте логи: `./deploy.sh logs`
2. Проверьте статус: `./deploy.sh status`
3. Создайте issue на GitHub: https://github.com/weae-g/CRM-military-hospital/issues

## Системные требования для разных нагрузок

### Малая нагрузка (до 10 пользователей)

- 2 CPU cores
- 2GB RAM
- 20GB HDD

### Средняя нагрузка (10-50 пользователей)

- 4 CPU cores
- 4GB RAM
- 50GB SSD

### Высокая нагрузка (50+ пользователей)

- 8+ CPU cores
- 8GB+ RAM
- 100GB+ SSD
- Настройте кластеризацию БД

---

**Успешного развертывания! 🚀**
