import pandas as pd

def read_excel_clinic(file_path, flag=False):
    """
    Чтение данных из Excel-файла для клиники и преобразование их в словарь.

    Функция загружает данные из Excel-файла, объединяет заголовки из первых двух строк,
    преобразует столбцы с датами в формат datetime, и при необходимости преобразует 
    их обратно в строки. Также добавляет столбец 'Койко-дни', если флаг не установлен.

    Args:
        file_path (str): Путь к Excel-файлу.
        flag (bool, optional): Если True, даты преобразуются в строки в формате 'дд.мм.гггг'. 
                               Если False, столбец 'Койко-дни' добавляется. По умолчанию False.

    Returns:
        list[dict]: Список словарей, представляющих строки Excel-файла, где каждый словарь 
                    соответствует одной строке и содержит преобразованные данные.
    """
    df = pd.read_excel(file_path)

    # Объединение первых двух строк заголовков
    new_headers = []
    for col1, col2 in zip(df.iloc[0], df.iloc[1]):
        if pd.isna(col1):
            new_headers.append(col2)
        elif pd.isna(col2):
            new_headers.append(col1)
        else:
            new_headers.append(f"{col1} {col2}")

    df.columns = new_headers
    df_filtered = df.iloc[2:].reset_index(drop=True)  # Пропуск первых двух строк с заголовками

    # Преобразование столбцов с датами
    date_columns = ['Дата обращения', 'Дата рождения', 'Госпитализация']
    for col in date_columns:
        if col in df_filtered.columns:
            df_filtered[col] = pd.to_datetime(df_filtered[col], errors='coerce', format='%d.%m.%Y')

    if flag:
        for col in date_columns:
            if col in df_filtered.columns:
                df_filtered[col] = df_filtered[col].apply(lambda x: x.strftime('%d.%m.%Y') if pd.notnull(x) and not isinstance(x, str) else x)
    else:
        df_filtered['Койко-дни'] = 0

    for col in date_columns:
        if col in df_filtered.columns:
            df_filtered[col] = df_filtered[col].apply(lambda x: x.strftime('%d.%m.%Y') if pd.notnull(x) and not isinstance(x, str) else x)

    data = df_filtered.to_dict(orient='records')

    return data

def read_excel_ds(file_path, flag=False):
    """
    Чтение данных из Excel-файла для диспансеризации и преобразование их в словарь.

    Функция загружает данные из Excel-файла, преобразует столбцы с датами в формат datetime, 
    и при необходимости преобразует их обратно в строки. Если флаг не установлен, вычисляет 
    количество койко-дней. Также добавляет поле 'highlight', если количество койко-дней больше 21.

    Args:
        file_path (str): Путь к Excel-файлу.
        flag (bool, optional): Если True, даты преобразуются в строки в формате 'дд.мм.гггг'. 
                               Если False, вычисляется количество койко-дней. По умолчанию False.

    Returns:
        list[dict]: Список словарей, представляющих строки Excel-файла, где каждый словарь 
                    соответствует одной строке и содержит преобразованные данные.
    """
    df = pd.read_excel(file_path)
    df_filtered = df.iloc[2:, :].reset_index(drop=True)
    df_filtered.columns = df.iloc[1, :].tolist()

    # Обновленный список столбцов с датами
    date_columns = ['Дата поступления', 'Дата выписки']

    # Преобразование столбцов с датами
    for col in date_columns:
        if col in df_filtered.columns:
            df_filtered[col] = pd.to_datetime(df_filtered[col], errors='coerce', format='%d.%m.%Y')

    # Если установлен флаг, преобразуем даты в строки
    if flag:
        for col in date_columns:
            if col in df_filtered.columns:
                df_filtered[col] = df_filtered[col].apply(lambda x: x.strftime('%d.%m.%Y') if pd.notnull(x) and not isinstance(x, str) else x)
    else:
        # Вычисление 'Койко-дни' при отсутствии флага
        if 'Дата поступления' in df_filtered.columns and 'Дата выписки' in df_filtered.columns:
            df_filtered['Койко-дни'] = df_filtered.apply(
                lambda row: (row['Дата выписки'] - row['Дата поступления']).days 
                if pd.notnull(row['Дата выписки']) and pd.notnull(row['Дата поступления']) 
                else 0, axis=1
            )
        else:
            df_filtered['Койко-дни'] = 0

    # Преобразование столбцов с датами в строки
    for col in date_columns:
        if col in df_filtered.columns:
            df_filtered[col] = df_filtered[col].apply(lambda x: x.strftime('%d.%m.%Y') if pd.notnull(x) and not isinstance(x, str) else x)

    data = df_filtered.to_dict(orient='records')

    # Добавление поля 'highlight' для строк, где 'Койко-дни' больше 21
    for row in data:
        row['highlight'] = row.get('Койко-дни', 0) > 21
        row['нарушение'] = False  # Можно добавить условие для отметки нарушений при необходимости

    return data

def read_excel(file_path, flag=False):
    """
    Чтение данных из Excel-файла и преобразование их в словарь с дополнительной проверкой нарушений.

    Args:
        file_path (str): Путь к Excel-файлу.
        flag (bool, optional): Если True, даты преобразуются в строки в формате 'дд.мм.гггг'. 
                               Если False, вычисляется количество койко-дней и проверяются нарушения. По умолчанию False.

    Returns:
        tuple: Кортеж из двух элементов:
            - list[dict]: Список словарей, представляющих строки Excel-файла, где каждый словарь 
                          соответствует одной строке и содержит преобразованные данные.
            - bool: Флаг, указывающий на наличие нарушения режима в данных.
    """
    # Чтение данных из Excel
    df = pd.read_excel(file_path)

    # Если первые строки содержат метаданные, удаляем их и обновляем заголовки
    df_filtered = df.iloc[2:].reset_index(drop=True)
    df_filtered.columns = df.iloc[1].tolist()

    # Проверка наличия необходимых столбцов
    date_columns = ['Дата госпитализации', 'Дата поступления', 'Дата выписки (убытия в часть)', 'Дата выписки']
    
    # Преобразование столбцов с датами в формат datetime
    for col in date_columns:
        if col in df_filtered.columns:
            df_filtered[col] = pd.to_datetime(df_filtered[col], errors='coerce', format='%d.%m.%Y')

    # Если флаг установлен, преобразуем даты обратно в строки
    if flag:
        for col in date_columns:
            if col in df_filtered.columns:
                df_filtered[col] = df_filtered[col].apply(
                    lambda x: x.strftime('%d.%m.%Y') if pd.notnull(x) else None
                )
    else:
        # Вычисление количества койко-дней
        if 'Дата госпитализации' in df_filtered.columns and 'Дата выписки (убытия в часть)' in df_filtered.columns:
            df_filtered['Койко-дни'] = df_filtered.apply(
                lambda row: (row['Дата выписки (убытия в часть)'] - row['Дата госпитализации']).days 
                if pd.notnull(row['Дата выписки (убытия в часть)']) and pd.notnull(row['Дата госпитализации']) 
                else 0, axis=1)
        else:
            df_filtered['Койко-дни'] = 0

    # Преобразование всех столбцов с датами обратно в строки
    for col in date_columns:
        if col in df_filtered.columns:
            df_filtered[col] = df_filtered[col].apply(
                lambda x: x.strftime('%d.%m.%Y') if pd.notnull(x) else None
            )

    # Преобразование DataFrame в список словарей
    data = df_filtered.to_dict(orient='records')

    # Проверка на наличие нарушений
    has_violation = any(row.get('ИСХОД') == 'Выписан за нарушение режима' for row in data)

    # Добавление дополнительных полей
    for row in data:
        row['highlight'] = row.get('Койко-дни', 0) > 21
        if not flag and 'ИСХОД' in row and row['ИСХОД'] == 'Выписан за нарушение режима':
            row['нарушение'] = True
        else:
            row['нарушение'] = False

    return data, has_violation


