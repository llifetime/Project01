# test_filter_by_currency.py
import unittest
from typing import List, Dict, Any, Iterator


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Фильтрует транзакции по валюте и возвращает итератор."""
    return (t for t in transactions if t.get("currency") == currency)


class TestFilterByCurrency(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {"amount": 100, "currency": "USD", "description": "Покупка в магазине"},
            {"amount": 200, "currency": "EUR", "description": "Оплата ресторана"},
            {"amount": 300, "currency": "USD", "description": "Перевод другу"},
            {"amount": 400, "currency": "GBP", "description": "Оплата отеля"},
        ]

    def test_filter_usd_transactions(self):
        """Тест: фильтрация транзакций в USD."""
        result = list(filter_by_currency(self.transactions, "USD"))
        expected = [
            {"amount": 100, "currency": "USD", "description": "Покупка в магазине"},
            {"amount": 300, "currency": "USD", "description": "Перевод другу"},
        ]
        self.assertEqual(result, expected)

    def test_filter_eur_transactions(self):
        """Тест: фильтрация транзакций в EUR."""
        result = list(filter_by_currency(self.transactions, "EUR"))
        expected = [{"amount": 200, "currency": "EUR", "description": "Оплата ресторана"}]
        self.assertEqual(result, expected)

    def test_no_matching_currency(self):
        """Тест: нет транзакций в заданной валюте (JPY)."""
        result = list(filter_by_currency(self.transactions, "JPY"))
        self.assertEqual(result, [])

    def test_empty_transactions_list(self):
        """Тест: пустой список транзакций."""
        result = list(filter_by_currency([], "USD"))
        self.assertEqual(result, [])

    def test_transactions_without_currency_key(self):
        """Тест: транзакции без ключа 'currency'."""
        test_data = [
            {"amount": 100, "description": "Покупка"},
            {"amount": 200, "currency": "EUR"},
            {"amount": 300, "currency": None},
        ]
        result = list(filter_by_currency(test_data, "USD"))
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
