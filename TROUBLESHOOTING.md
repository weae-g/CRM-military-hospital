# Устранение неполадок CRM Hospital

## 🔴 502 Bad Gateway - Самая частая проблема!

### Быстрое решение (работает в 90% случаев):

```bash
# 1. Проверьте логи web контейнера
docker-compose logs web

# 2. Проверьте файл конфигурации
nano website/app/.env

# Убедитесь, что DATABASE_URL правильный:
# DATABASE_URL=postgresql://postgres:ваш_пароль@db:5432/Patients
# ВАЖНО: должно быть @db, а НЕ @localhost!

# 3. Перезапустите web контейнер
docker-compose restart web

# 4. Подождите 10 секунд
sleep 10

# 5. Проверьте снова
curl http://localhost
```

---

## Диагностика по шагам

### 1️⃣ Проверьте статус контейнеров

```bash
docker-compose ps
```

**Что должно быть:**

```
NAME                  STATUS
crm_hospital_db       Up (healthy)
crm_hospital_web      Up
crm_hospital_nginx    Up
```

**Если web контейнер в статусе "Exit" или "Restarting":**

```bash
# Смотрим логи
docker-compose logs web

# Обычно это ошибка подключения к БД или ошибка в коде
```

---

### 2️⃣ Проверьте подключение к базе данных

```bash
# Попробуйте подключиться к БД из web контейнера
docker-compose exec web python -c "
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('website/app/.env')
url = os.getenv('DATABASE_URL')
print(f'Trying to connect to: {url}')

engine = create_engine(url)
conn = engine.connect()
print('✓ Connection successful!')
conn.close()
"
```

**Если ошибка "could not connect to server":**

Проблема в DATABASE_URL. Проверьте файл:

```bash
cat website/app/.env

# Должно быть:
DATABASE_URL=postgresql://postgres:пароль@db:5432/Patients

# НЕ должно быть:
# DATABASE_URL=postgresql://postgres:пароль@localhost:5432/Patients (неправильно!)
```

Исправьте и перезапустите:

```bash
nano website/app/.env
docker-compose restart web
```

---

### 3️⃣ Проверьте доступность FastAPI напрямую

```bash
# Попробуйте обратиться к FastAPI минуя nginx
curl http://localhost:8000

# Если работает - проблема в nginx
# Если не работает - проблема в web контейнере
```

**Если FastAPI отвечает, но через nginx 502:**

Проблема в nginx конфигурации:

```bash
# Проверьте конфигурацию nginx
cat nginx.conf

# Убедитесь, что upstream указывает на web:8000
# upstream web_backend {
#     server web:8000;
# }

# Перезапустите nginx
docker-compose restart nginx
```

---

### 4️⃣ Типичные ошибки и решения

#### ❌ Ошибка: "PermissionError: [Errno 13] Permission denied: '/temp'"

```bash
# Проблема: приложение не может создать директорию

# Решение 1: Пересоберите образ с исправленным Dockerfile
docker-compose down
docker-compose build --no-cache web
docker-compose up -d

# Решение 2: Создайте директорию вручную (временное решение)
docker-compose exec -u root web mkdir -p /app/temp
docker-compose exec -u root web chown -R appuser:appuser /app/temp
docker-compose restart web
```

#### ❌ Ошибка: "Module not found"

```bash
# Пересоберите образ
docker-compose down
docker-compose build --no-cache web
docker-compose up -d
```

#### ❌ Ошибка: "Address already in use"

```bash
# Порт занят другим процессом
sudo lsof -i :80
sudo lsof -i :8000

# Остановите процесс или измените порт в .env
nano .env
# Измените NGINX_PORT=8080
docker-compose up -d
```

#### ❌ Ошибка: "Permission denied"

```bash
# Проблема с правами на файлы
sudo chown -R $USER:$USER .
chmod +x deploy.sh
```

#### ❌ База данных не создалась

```bash
# Пересоздайте БД
docker-compose down -v  # Удалит volumes!
docker-compose up -d

# Или создайте вручную
docker-compose exec db psql -U postgres -c "CREATE DATABASE Patients;"
```

---

## 📊 Полезные команды для диагностики

```bash
# Логи всех сервисов
docker-compose logs

# Логи в реальном времени
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# Поиск ошибок
docker-compose logs web | grep -i error
docker-compose logs web | grep -i exception

# Войти в контейнер
docker-compose exec web bash
docker-compose exec db sh

# Перезапуск
docker-compose restart web
docker-compose restart

# Полная перезагрузка
./deploy.sh restart

# Статус ресурсов
docker stats

# Проверка сети
docker network ls
docker network inspect crm-military-hospital_crm_network
```

---

## 🔧 Полная переустановка (если ничего не помогло)

```bash
# 1. Остановите и удалите все
docker-compose down -v
docker system prune -a

# 2. Проверьте конфигурацию
nano .env
nano website/app/.env

# 3. Запустите заново
./deploy.sh start

# 4. Проверьте логи
docker-compose logs -f
```

---

## 📞 Контрольный список

Перед обращением за помощью, проверьте:

- [ ] Все три контейнера в статусе "Up": `docker-compose ps`
- [ ] Файл `.env` существует и содержит пароль БД
- [ ] Файл `website/app/.env` существует и содержит правильный DATABASE_URL с `@db`
- [ ] Пароли совпадают в обоих .env файлах
- [ ] Порты 80, 8000, 5432 не заняты: `sudo netstat -tulpn`
- [ ] В логах web нет ошибок: `docker-compose logs web`
- [ ] FastAPI отвечает: `curl http://localhost:8000`
- [ ] База данных доступна: `docker-compose exec db psql -U postgres -d Patients -c "SELECT 1;"`

---

## 🆘 Всё ещё не работает?

1. Соберите диагностическую информацию:

```bash
# Сохраните в файл
./deploy.sh status > diagnostic.txt
docker-compose logs >> diagnostic.txt
cat .env >> diagnostic.txt
cat website/app/.env >> diagnostic.txt
```

2. Создайте issue на GitHub с файлом diagnostic.txt:
   https://github.com/weae-g/CRM-military-hospital/issues

---

**Удачи! 🍀**
