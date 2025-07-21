from datetime import datetime
from typing import List, Dict, Optional


def filter_by_state(
        transactions: List[Dict],
        state: Optional[str] = "EXECUTED"
) -> List[Dict]:
    """Фильтрует транзакции по указанному статусу.

    Args:
        transactions: Список словарей с транзакциями
        state: Статус для фильтрации ("EXECUTED", "PENDING", "FAILED"),
               или None для транзакций без статуса

    Returns:
        Список транзакций с указанным статусом
    """
    if not transactions:
        return []

    if state is None:
        return [t for t in transactions if "state" not in t]

    return [t for t in transactions if t.get("state") == state]


def sort_by_date(
        transactions: List[Dict],
        reverse: bool = False
) -> List[Dict]:
    """Сортирует транзакции по дате."""

    def get_date(t):
        date_str = t.get("date", "")
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            return datetime.min if not reverse else datetime.max

    return sorted(transactions, key=get_date, reverse=reverse)
