import unittest
from src.generators import transaction_descriptions  # Импортируем тестируемую функцию


class TestTransactionDescriptions(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.transactions = [
            {"amount": 100, "currency": "USD", "description": "Purchase"},
            {"amount": 200, "currency": "EUR", "description": "Withdrawal"},
            {"amount": 300, "currency": "USD"},  # Нет описания
            {"amount": 400, "currency": "GBP", "description": ""},  # Пустое описание
            {"amount": 500, "currency": "USD", "description": "Deposit"},
        ]

    def test_get_all_descriptions(self):
        """Тест получения всех описаний"""
        result = list(transaction_descriptions(self.transactions))
        expected = ["Purchase", "Withdrawal", "", "", "Deposit"]
        self.assertEqual(result, expected)

    def test_empty_transactions(self):
        """Тест с пустым списком транзакций"""
        result = list(transaction_descriptions([]))
        self.assertEqual(result, [])

    def test_no_description_field(self):
        """Тест с транзакциями без поля description"""
        transactions = [
            {"amount": 100, "currency": "USD"},
            {"amount": 200, "description": "Payment"},
        ]
        result = list(transaction_descriptions(transactions))
        expected = ["", "Payment"]
        self.assertEqual(result, expected)

    def test_iterator_behavior(self):
        """Тест проверяет, что функция возвращает генератор"""
        result = transaction_descriptions(self.transactions)
        self.assertTrue(hasattr(result, '__iter__'))
        self.assertFalse(isinstance(result, list))  # Это именно генератор, не список

    def test_lazy_evaluation(self):
        """Тест ленивой оценки генератора"""
        # Создаем мок-транзакции с "побочным эффектом"
        class MockTransaction:
            def __getitem__(self, key):
                if key == "description":
                    return "Mock"
                raise KeyError(key)

        transactions = [MockTransaction()]
        result = transaction_descriptions(transactions)
        # Если бы не ленивая оценка, здесь уже возникла бы ошибка
        self.assertEqual(next(result), "Mock")


if __name__ == '__main__':
    unittest.main()
