from typing import Dict, Iterator, List


def card_number_generator(start: int = 1, end: int = 9999_9999_9999_9999) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    :param start: Начальное значение (от 1)
    :param end: Конечное значение (до 9999_9999_9999_9999)
    :raises ValueError: Если start > end
    """
    if start > end:
        raise ValueError("Start value cannot be greater than end value")

    for number in range(start, end + 1):
        card_num = f"{number:016d}"
        yield f"{card_num[:4]} {card_num[4:8]} {card_num[8:12]} {card_num[12:16]}"


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    return (tx for tx in transactions if tx.get("currency") == currency)


def transaction_descriptions(transactions):
    for tx in transactions:
        description = tx["description"] if "description" in tx else ""
        yield description
