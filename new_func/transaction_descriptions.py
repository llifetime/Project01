import unittest
from typing import List, Dict, Any, Generator


# Определяем тестируемую функцию
def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """Генератор, возвращающий описания транзакций."""
    for transaction in transactions:
        yield transaction.get('description')


class TestTransactionDescriptions(unittest.TestCase):
    def setUp(self):
        # Стандартные тестовые данные
        self.transactions = [
            {"amount": 100, "currency": "USD", "description": "Покупка в магазине"},
            {"amount": 200, "currency": "EUR", "description": "Оплата ресторана"},
            {"amount": 300, "currency": "USD", "description": "Перевод другу"},
        ]

    def test_returns_all_descriptions(self):
        """Проверяет получение всех описаний из списка транзакций"""
        result = list(transaction_descriptions(self.transactions))
        expected = [
            "Покупка в магазине",
            "Оплата ресторана",
            "Перевод другу"
        ]
        self.assertEqual(result, expected)

    def test_empty_transactions_list(self):
        """Проверяет работу с пустым списком транзакций"""
        result = list(transaction_descriptions([]))
        self.assertEqual(result, [])

    def test_transactions_without_descriptions(self):
        """Проверяет обработку транзакций без описаний"""
        test_data = [
            {"amount": 100, "currency": "USD"},
            {"amount": 200, "description": None},
            {"description": ""},
        ]
        result = list(transaction_descriptions(test_data))
        expected = [None, None, ""]
        self.assertEqual(result, expected)

    def test_mixed_transactions(self):
        """Проверяет работу со смешанными данными"""
        test_data = [
            {"amount": 100},
            {"description": "Тестовая транзакция"},
            {"amount": 200, "description": None},
        ]
        result = list(transaction_descriptions(test_data))
        expected = [None, "Тестовая транзакция", None]
        self.assertEqual(result, expected)

    def test_single_transaction(self):
        """Проверяет обработку единственной транзакции"""
        test_data = [{"description": "Одиночная операция"}]
        result = list(transaction_descriptions(test_data))
        self.assertEqual(result, ["Одиночная операция"])


if __name__ == "__main__":
    unittest.main()
