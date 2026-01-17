"""
Скрипт для инициализации базы данных - создание всех таблиц
"""
import sys
import os

# Добавляем путь к приложению
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'website'))

from website.app.model.database.database import Base, engine

# Импортируем все модели, чтобы они были зарегистрированы в Base.metadata
try:
    from website.app.model.pacient_hospital import models as pacient_hospital_models
except ImportError as e:
    print(f"Не удалось импортировать pacient_hospital.models: {e}")

try:
    from website.app.model.user import models as user_models
except ImportError as e:
    print(f"Не удалось импортировать user.models: {e}")

try:
    from website.app.model.vpd import models as vpd_models
except ImportError as e:
    print(f"Не удалось импортировать vpd.models: {e}")

try:
    from website.app.model.vvk import models as vvk_models
except ImportError as e:
    print(f"Не удалось импортировать vvk.models: {e}")

try:
    from website.app.model.сlinic import models as clinic_models
except ImportError as e:
    print(f"Не удалось импортировать clinic.models: {e}")

try:
    from website.app.model.documents import models as documents_models
except ImportError as e:
    print(f"Не удалось импортировать documents.models: {e}")

try:
    from website.app.model.Gallery import models as gallery_models
except ImportError as e:
    print(f"Не удалось импортировать Gallery.models: {e}")

try:
    from website.app.model.settings import models as settings_models
except ImportError as e:
    print(f"Не удалось импортировать settings.models: {e}")

def init_db():
    """Создать все таблицы в базе данных"""
    print("Создание таблиц в базе данных...")
    print(f"Database URL: {engine.url}")
    
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    
    print("✅ Все таблицы успешно созданы!")
    
    # Вывести список созданных таблиц
    print("\nСписок созданных таблиц:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")

if __name__ == "__main__":
    init_db()
