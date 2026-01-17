"""
Скрипт для инициализации базы данных - создание всех таблиц
"""
from model.database.database import Base, engine

# Импортируем все модели, чтобы они были зарегистрированы в Base.metadata
try:
    from model.pacient_hospital import models as pacient_hospital_models
    print("✓ Импортированы модели pacient_hospital")
except ImportError as e:
    print(f"⚠ Не удалось импортировать pacient_hospital.models: {e}")

try:
    from model.user import models as user_models
    print("✓ Импортированы модели user")
except ImportError as e:
    print(f"⚠ Не удалось импортировать user.models: {e}")

try:
    from model.vpd import models as vpd_models
    print("✓ Импортированы модели vpd")
except ImportError as e:
    print(f"⚠ Не удалось импортировать vpd.models: {e}")

try:
    from model.vvk import models as vvk_models
    print("✓ Импортированы модели vvk")
except ImportError as e:
    print(f"⚠ Не удалось импортировать vvk.models: {e}")

try:
    from model.сlinic import models as clinic_models
    print("✓ Импортированы модели clinic")
except ImportError as e:
    print(f"⚠ Не удалось импортировать clinic.models: {e}")

try:
    from model.documents import models as documents_models
    print("✓ Импортированы модели documents")
except ImportError as e:
    print(f"⚠ Не удалось импортировать documents.models: {e}")

try:
    from model.Gallery import models as gallery_models
    print("✓ Импортированы модели Gallery")
except ImportError as e:
    print(f"⚠ Не удалось импортировать Gallery.models: {e}")

try:
    from model.settings import models as settings_models
    print("✓ Импортированы модели settings")
except ImportError as e:
    print(f"⚠ Не удалось импортировать settings.models: {e}")

def init_db():
    """Создать все таблицы в базе данных"""
    print("\n" + "="*60)
    print("Создание таблиц в базе данных...")
    print(f"Database URL: {engine.url}")
    print("="*60 + "\n")
    
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    
    print("\n" + "="*60)
    print("✅ Все таблицы успешно созданы!")
    print("="*60 + "\n")
    
    # Вывести список созданных таблиц
    if Base.metadata.sorted_tables:
        print("Список созданных таблиц:")
        for table in Base.metadata.sorted_tables:
            print(f"  ✓ {table.name}")
        print(f"\nВсего таблиц: {len(Base.metadata.sorted_tables)}")
    else:
        print("⚠ Таблицы не были созданы. Проверьте модели.")

if __name__ == "__main__":
    init_db()
