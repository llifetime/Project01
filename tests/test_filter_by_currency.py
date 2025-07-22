import unittest
from src.generators import filter_by_currency  # Импортируем тестируемую функцию


class TestFilterByCurrency(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.transactions = [
            {"amount": 100, "currency": "USD", "description": "Purchase"},
            {"amount": 200, "currency": "EUR", "description": "Withdrawal"},
            {"amount": 300, "currency": "USD", "description": "Transfer"},
            {"amount": 400, "currency": "GBP", "description": "Payment"},
            {"amount": 500, "currency": "USD", "description": "Deposit"},
        ]

    def test_filter_usd(self):
        """Тест фильтрации USD транзакций"""
        result = list(filter_by_currency(self.transactions, "USD"))
        expected = [
            {"amount": 100, "currency": "USD", "description": "Purchase"},
            {"amount": 300, "currency": "USD", "description": "Transfer"},
            {"amount": 500, "currency": "USD", "description": "Deposit"},
        ]
        self.assertEqual(result, expected)

    def test_filter_eur(self):
        """Тест фильтрации EUR транзакций"""
        result = list(filter_by_currency(self.transactions, "EUR"))
        expected = [{"amount": 200, "currency": "EUR", "description": "Withdrawal"}]
        self.assertEqual(result, expected)

    def test_empty_result(self):
        """Тест на пустой результат при отсутствии валюты"""
        result = list(filter_by_currency(self.transactions, "JPY"))
        self.assertEqual(result, [])

    def test_empty_input(self):
        """Тест на пустом списке транзакций"""
        result = list(filter_by_currency([], "USD"))
        self.assertEqual(result, [])

    def test_missing_currency_field(self):
        """Тест обработки транзакций без поля currency"""
        transactions = [
            {"amount": 100, "description": "Purchase"},
            {"amount": 200, "currency": "USD"},
        ]
        result = list(filter_by_currency(transactions, "USD"))
        expected = [{"amount": 200, "currency": "USD"}]
        self.assertEqual(result, expected)

    def test_iterator_behavior(self):
        """Тест проверяет, что функция возвращает итератор"""
        result = filter_by_currency(self.transactions, "USD")
        self.assertTrue(hasattr(result, '__iter__'))
        self.assertFalse(hasattr(result, '__len__'))  # Итератор не имеет длины

    def test_case_sensitivity(self):
        """Тест на чувствительность к регистру валюты"""
        transactions = [
            {"amount": 100, "currency": "usd"},
            {"amount": 200, "currency": "USD"},
        ]
        result = list(filter_by_currency(transactions, "USD"))
        expected = [{"amount": 200, "currency": "USD"}]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
