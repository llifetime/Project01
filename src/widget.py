from datetime import datetime
import re


def mask_card(card_info: str) -> str:
    """
    Маскирует номер карты или счета:

    """
    # Удаляем все нецифровые символы
    digits = ''.join(filter(str.isdigit, card_info))

    # Если нет цифр или есть буквы - возвращаем исходную строку
    if not digits or any(c.isalpha() for c in card_info):
        return card_info

    length = len(digits)

    # Карта (16-19 цифр)
    if 16 <= length <= 19:
        if length == 16:
            return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
        else:
            return f"{digits[:4]} {digits[4:8]} **** **** {digits[-4:]}"

    # Счет (10+ цифр, кроме 16-19)
    elif length >= 10:
        return f"**{digits[-4:]}"

    # Другие случаи (не маскируем)
    else:
        return card_info


def get_date(input_str: str) -> datetime | None:
    """
    Извлекает дату из строки с правильным определением порядка дня и месяца
    """
    if not input_str or not isinstance(input_str, str):
        return None


    patterns = [
        # ISO format (YYYY-MM-DD)
        (r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})', 'YMD'),
        # DD.MM.YYYY (интерпретируем как день.месяц.год)
        (r'(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})', 'DMY'),
        # YYYY/MM/DD
        (r'(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})', 'YMD'),
        # Month abbreviations (Oct 5 2023, Oct 5, 2023)
        (r'(?P<month>[A-Za-z]{3})\s+(?P<day>\d{1,2}),?\s+(?P<year>\d{4})', 'MDY'),
        # Full month names (5 October 2023)
        (r'(?P<day>\d{1,2})\s+(?P<month>[A-Za-z]+)\s+(?P<year>\d{4})', 'DMY')
    ]

    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        **{m.lower(): i + 1 for i, m in enumerate([
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ])}
    }

    for pattern, order in patterns:
        match = re.search(pattern, input_str, re.IGNORECASE)
        if not match:
            continue

        try:
            groups = match.groupdict()
            year = int(groups['year'])

            # Обработка текстовых месяцев
            if groups['month'].isalpha():
                month = month_map.get(groups['month'].lower())
                if month is None:
                    continue
            else:
                month = int(groups['month'])

            day = int(groups['day'])

            # Для форматов с точкой (DD.MM.YYYY) и полными названиями месяцев (5 October 2023)
            # оставляем день и месяц как есть (не меняем местами)
            if order == 'DMY':
                pass  # день и месяц уже в правильном порядке
            elif order == 'MDY':
                pass  # месяц и день уже в правильном порядке
            elif order == 'YMD':
                pass  # год, месяц, день уже в правильном порядке

            # Валидация даты
            try:
                return datetime(year, month, day)
            except ValueError:
                continue

        except (ValueError, KeyError):
            continue

    return None
