#!/bin/bash

# Скрипт автоматического развертывания CRM Hospital на Linux сервере
# Использование: ./deploy.sh [start|stop|restart|logs|update]

set -e  # Останавливаться при ошибках

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка наличия Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker не установлен!"
        log_info "Установите Docker: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose не установлен!"
        log_info "Установите Docker Compose: apt-get install docker-compose-plugin"
        exit 1
    fi
    
    log_info "Docker и Docker Compose установлены ✓"
}

# Проверка .env файла
check_env() {
    if [ ! -f .env.production ]; then
        log_error "Файл .env.production не найден!"
        log_info "Создайте файл .env.production на основе .env.production.example"
        exit 1
    fi
    
    # Копируем .env.production в .env если его нет
    if [ ! -f .env ]; then
        cp .env.production .env
        log_info "Создан файл .env из .env.production"
    fi
    
    log_info "Конфигурационные файлы найдены ✓"
}

# Запуск приложения
start_app() {
    log_info "Запуск приложения..."
    
    # Создаем необходимые директории
    mkdir -p website/app/logs
    mkdir -p data/exchange
    
    # Останавливаем старые контейнеры если есть
    docker-compose down 2>/dev/null || true
    
    # Собираем и запускаем контейнеры
    log_info "Сборка Docker образов..."
    docker-compose build
    
    log_info "Запуск контейнеров..."
    docker-compose up -d
    
    log_info "Ожидание запуска сервисов..."
    sleep 10
    
    # Проверка статуса
    if docker-compose ps | grep -q "Up"; then
        log_info "Приложение успешно запущено! ✓"
        log_info "Доступ к приложению: http://$(hostname -I | awk '{print $1}'):80"
        log_info "API документация: http://$(hostname -I | awk '{print $1}'):80/docs"
    else
        log_error "Ошибка при запуске приложения"
        docker-compose logs
        exit 1
    fi
}

# Остановка приложения
stop_app() {
    log_info "Остановка приложения..."
    docker-compose down
    log_info "Приложение остановлено ✓"
}

# Перезапуск приложения
restart_app() {
    log_info "Перезапуск приложения..."
    stop_app
    start_app
}

# Просмотр логов
show_logs() {
    log_info "Логи приложения (Ctrl+C для выхода):"
    docker-compose logs -f
}

# Обновление приложения
update_app() {
    log_info "Обновление приложения..."
    
    # Останавливаем контейнеры
    docker-compose down
    
    # Обновляем код (если используется git)
    if [ -d .git ]; then
        log_info "Обновление кода из Git..."
        git pull
    fi
    
    # Пересобираем и запускаем
    log_info "Пересборка образов..."
    docker-compose build --no-cache
    
    log_info "Запуск обновленного приложения..."
    docker-compose up -d
    
    log_info "Приложение обновлено ✓"
}

# Статус приложения
status_app() {
    log_info "Статус сервисов:"
    docker-compose ps
}

# Резервное копирование базы данных
backup_db() {
    log_info "Создание резервной копии базы данных..."
    
    BACKUP_DIR="./backups"
    mkdir -p $BACKUP_DIR
    
    BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    docker-compose exec -T db pg_dump -U postgres Patients > $BACKUP_FILE
    
    if [ -f $BACKUP_FILE ]; then
        log_info "Резервная копия создана: $BACKUP_FILE ✓"
    else
        log_error "Ошибка создания резервной копии"
        exit 1
    fi
}

# Главное меню
case "${1:-help}" in
    start)
        check_docker
        check_env
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        restart_app
        ;;
    logs)
        show_logs
        ;;
    update)
        check_docker
        update_app
        ;;
    status)
        status_app
        ;;
    backup)
        backup_db
        ;;
    *)
        echo "Использование: $0 {start|stop|restart|logs|update|status|backup}"
        echo ""
        echo "Команды:"
        echo "  start   - Запустить приложение"
        echo "  stop    - Остановить приложение"
        echo "  restart - Перезапустить приложение"
        echo "  logs    - Показать логи приложения"
        echo "  update  - Обновить и перезапустить приложение"
        echo "  status  - Показать статус сервисов"
        echo "  backup  - Создать резервную копию базы данных"
        exit 1
        ;;
esac
