from src.widget import mask_card

from src.widget import get_date  # Импортируем тестируемую функцию
from datetime import datetime

import pytest


@pytest.mark.parametrize("input_data, expected", [
    # Тесты для карт (16-19 цифр)
    ("1234567890123456", "1234 56** **** 3456"),  # 16 цифр
    ("12345678901234567", "1234 5678 **** **** 4567"),  # 17 цифр (изменено ожидание)
    ("1234 5678 9012 3456", "1234 56** **** 3456"),  # с пробелами
    ("1234-5678-9012-3456", "1234 56** **** 3456"),  # с дефисами

    # Тесты для счетов
    ("12345678901234567890", "**7890"),  # 20 цифр
    ("1234567890", "**7890"),  # 10 цифр

    # Короткие номера
    ("12345", "12345"),  # 5 цифр

    # Некорректные данные
    ("", ""),
    ("abc123", "abc123"),
    ("1234 5678 abcd 3456", "1234 5678 abcd 3456"),
])
def test_mask_card(input_data, expected):
    assert mask_card(input_data) == expected


@pytest.mark.parametrize("input_date, expected", [
    # Стандартные форматы дат
    ("2023-10-05", datetime(2023, 10, 5)),
    ("05.10.2023", datetime(2023, 10, 5)),
    ("2023/10/05", datetime(2023, 10, 5)),
    ("Oct 5 2023", datetime(2023, 10, 5)),
    ("5 October 2023", datetime(2023, 10, 5)),

    # Граничные случаи дат
    ("2023-02-28", datetime(2023, 2, 28)),  # Не високосный год
    ("2024-02-29", datetime(2024, 2, 29)),  # Високосный год
    ("2023-12-31", datetime(2023, 12, 31)),  # Последний день года
    ("2023-01-01", datetime(2023, 1, 1)),  # Первый день года

    # Нестандартные строки с датами
    ("Date: 2023-10-05", datetime(2023, 10, 5)),
    ("Posted on Oct 5, 2023", datetime(2023, 10, 5)),
    ("2023-10-05T12:34:56", datetime(2023, 10, 5)),
    ("The event starts 05.10.2023", datetime(2023, 10, 5)),

    # Отсутствие даты в строке
    ("No date here", None),
    ("", None),
    ("Just random text 123", None),

    # Некорректные даты
    ("2023-13-01", None),  # Несуществующий месяц
    ("2023-02-30", None),  # Несуществующий день
    ("32.01.2023", None),  # Несуществующий день
])
def test_get_date(input_date, expected):
    result = get_date(input_date)
    assert result == expected, f"Для входных данных '{input_date}' ожидалось {expected}, получено {result}"
