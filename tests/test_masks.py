from src.masks import get_mask_card_number
import pytest


def test_get_mask_card_number_default():
    """Тест для проверки маскирования номера карты по умолчанию"""
    assert get_mask_card_number("1234567890128912") == "1234 56** **** 8912"


@pytest.mark.parametrize("value, expected", [
    ("35383033474447895560", "3538 30** **** 5560"),
    ("73654108430135874305", "7365 41** **** 4305"),
    ("73654108430ppsdslala", "Неверный номер счета"),
    ("[f[f[asdasdqwe[f[f[f", "Неверный номер счета"),
    ("", "Неверный номер счета"),
])
def test_get_mask_card_number_cases(value, expected):
    """Параметризованный тест для разных случаев"""
    assert get_mask_card_number(value) == expected
