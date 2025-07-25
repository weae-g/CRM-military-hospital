import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model.сlinic.models import ClinicData, Base, get_moscow_time  # замените на ваш модуль
from app.model.database.database import SessionLocal
from datetime import datetime
# Чтение данных из Excel-файла
file_path = 'C:\\Users\\421\\Desktop\\321.xlsx'  # замените на путь к вашему файлу
df = pd.read_excel(file_path)



# Настройка соединения с базой данных
DATABASE_URL = 'postgresql://postgres:1111@localhost/Patients'  # замените на ваш URL базы данных
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
# Замена NaN значений на None
df = df.where(pd.notnull(df), None)

# Преобразование всех значений в строки
df = df.astype(str)

# Функция для преобразования даты
def parse_date(date_str):
    if isinstance(date_str, datetime):
        return date_str
    try:
        return datetime.strptime(date_str, '%d.%m.%Y') if date_str else None
    except ValueError:
        return None

# Обработка и добавление данных в базу данных
for index, row in df.iterrows():
    card_number = str(row['Номер карты']) if row['Номер карты'] is not None else None
    full_name = str(row['ФИО']) if row['ФИО'] is not None else None
    birthday = parse_date(row['Дата рождения']) if row['Дата рождения'] is not None else None
    phone_number = str(row['Номер телефона']) if row['Номер телефона'] is not None else None
    military_rank = str(row['звание']) if row['звание'] is not None else None

    # Проверка и установка текущего времени
    try:
        current_time = get_moscow_time()
    except Exception as e:
        print(f"Error getting current time: {e}")
        current_time = None

    # Создание объекта ClinicData
    clinic_data = ClinicData(
        card_number=card_number,
        full_name=full_name,
        birthday=birthday,
        phone_number=phone_number,
        military_rank=military_rank,
        current_time=current_time
    )

    try:
        session.add(clinic_data)
    except Exception as e:
        print(f"DataError for row {index}: {e}")
        session.rollback()  # Откатить транзакцию, если ошибка
    except Exception as e:
        print(f"Unexpected error for row {index}: {e}")
        session.rollback()  # Откатить транзакцию, если ошибка

# Сохранение изменений в базе данных
try:
    session.commit()
except Exception as e:
    print(f"Commit error: {e}")
    session.rollback()
finally:
    session.close()