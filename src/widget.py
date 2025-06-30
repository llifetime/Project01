from datetime import datetime


def mask_card(card_info: str) -> str:
    """
    Маскирует номер карты, оставляя последние 4 цифры видимыми
    Пример: Visa Platinum 7000792289606361 -> Visa Platinum **** **** **** 6361
    """
    # Разделяем тип и номер

    parts = card_info.split()
    if len(parts) != 2:
        raise ValueError("Некорректный формат карты")

    card_type = parts[0]
    card_number = parts[1]

    # Маскируем номер
    masked_number = f"{card_type} {'*' * 12}{card_number[-4:]}"
    return masked_number


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
