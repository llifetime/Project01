from datetime import datetime


def mask_card(card_info: str) -> str:
    """
    Правильно маскирует карту, даже если в названии несколько слов.
    Пример: Visa Platinum 7000792289606361 -> Visa Platinum 7000 79** **** 6361
    """
    parts = card_info.split()
    if len(parts) < 2:
        raise ValueError("Некорректный формат карты. Ожидалось название и номер.")

    # Номер всегда последний элемент, остальное — тип карты
    card_number = parts[-1]
    card_type = " ".join(parts[:-1])

    if not card_number.isdigit() or len(card_number) < 16:
        raise ValueError("Номер карты должен состоять минимум из 16 цифр")

    # Коммерческий стандарт маскирования: разделение по 4 цифры
    return f"{card_type} {card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"



def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата "2024-03-11T02:26:18.671407" в формат "11.03.2024"

    Параметры:
    date_string (str): строка с датой в формате ISO

    Возвращает:
    str: дата в формате "ДД.ММ.ГГГГ"
    """
    try:
        # Разбираем входную строку в объект datetime
        dt = datetime.fromisoformat(date_string)

        # Форматируем в нужный формат
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Некорректный формат даты. Ожидался формат 'YYYY-MM-DDTHH:MM:SS.ffffff'")
