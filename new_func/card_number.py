import unittest
from typing import Generator


# Определяем тестируемую функцию
def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX"""
    for number in range(start, end + 1):
        yield f"{number:016d}"[:16]  # Форматируем с ведущими нулями


class TestCardNumberGenerator(unittest.TestCase):
    def test_normal_range(self):
        """Тестирование обычного диапазона"""
        generator = card_number_generator(1, 5)
        result = list(generator)
        expected = [
            "0000000000000001",
            "0000000000000002",
            "0000000000000003",
            "0000000000000004",
            "0000000000000005"
        ]
        self.assertEqual(result, expected)

    def test_format_correctness(self):
        """Проверка корректности форматирования"""
        generator = card_number_generator(9999999999999999, 9999999999999999)
        result = next(generator)
        self.assertEqual(result, "9999999999999999")
        self.assertEqual(len(result), 16)  # Всегда 16 цифр

    def test_edge_cases(self):
        """Проверка крайних значений"""
        # Первый возможный номер
        first_num = next(card_number_generator(1, 1))
        self.assertEqual(first_num, "0000000000000001")

        # Последний возможный номер
        last_num = next(card_number_generator(9999999999999999, 9999999999999999))
        self.assertEqual(last_num, "9999999999999999")

    def test_empty_range(self):
        """Проверка пустого диапазона (start > end)"""
        generator = card_number_generator(10, 5)
        result = list(generator)
        self.assertEqual(result, [])

    def test_single_value(self):
        """Проверка генерации одного значения"""
        generator = card_number_generator(42, 42)
        result = list(generator)
        self.assertEqual(result, ["0000000000000042"])

    def test_large_range(self):
        """Проверка большого диапазона (первые 3 значения)"""
        generator = card_number_generator(1, 1000)
        first_three = [next(generator) for _ in range(3)]
        self.assertEqual(first_three, [
            "0000000000000001",
            "0000000000000002",
            "0000000000000003"
        ])

    def test_number_length(self):
        """Все номера должны иметь длину 16 символов"""
        generator = card_number_generator(123, 125)
        for number in generator:
            self.assertEqual(len(number), 16)
            self.assertTrue(number.isdigit())


if __name__ == "__main__":
    unittest.main()
