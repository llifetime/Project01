from typing import Dict, Iterator, List


def card_number_generator(start: int = 1, end: int = 9999_9999_9999_9999) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    :param start: Начальное значение (от 1)
    :param end: Конечное значение (до 9999_9999_9999_9999)
    :yield: Номер карты в формате строки с пробелами
    """
    for number in range(start, end + 1):
        # Форматируем число в 16-значную строку с ведущими нулями
        card_num = f"{number:016d}"
        # Разбиваем на группы по 4 цифры с пробелами
        yield f"{card_num[:4]} {card_num[4:8]} {card_num[8:12]} {card_num[12:16]}"


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    return (tx for tx in transactions if tx.get("currency") == currency)


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    return (tx.get("description", "") for tx in transactions)
