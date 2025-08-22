import unittest
from src.generators import card_number_generator  # Импортируем тестируемый генератор


class TestCardNumberGenerator(unittest.TestCase):
    def test_single_card_generation(self):
        """Тест генерации одного номера карты"""
        generator = card_number_generator(1, 1)
        result = next(generator)
        self.assertEqual(result, "0000 0000 0000 0001")

    def test_range_generation(self):
        """Тест генерации диапазона номеров"""
        generator = card_number_generator(1, 5)
        results = list(generator)
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005"
        ]
        self.assertEqual(results, expected)

    def test_large_numbers(self):
        """Тест генерации больших номеров"""
        generator = card_number_generator(9999_9999_9999_9995, 9999_9999_9999_9999)
        results = list(generator)
        expected = [
            "9999 9999 9999 9995",
            "9999 9999 9999 9996",
            "9999 9999 9999 9997",
            "9999 9999 9999 9998",
            "9999 9999 9999 9999"
        ]
        self.assertEqual(results, expected)

    def test_format_correctness(self):
        """Тест правильности формата номера карты"""
        generator = card_number_generator(1234_5678_9012_3456, 1234_5678_9012_3456)
        result = next(generator)
        self.assertEqual(result, "1234 5678 9012 3456")
        self.assertEqual(len(result), 19)  # 16 цифр + 3 пробела
        self.assertTrue(all(c.isdigit() or c == ' ' for c in result))

    def test_generator_type(self):
        """Тест, что функция возвращает генератор"""
        gen = card_number_generator(1, 5)
        self.assertTrue(hasattr(gen, '__iter__'))
        self.assertTrue(hasattr(gen, '__next__'))

    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Минимальное значение
        gen_min = card_number_generator(0, 0)
        self.assertEqual(next(gen_min), "0000 0000 0000 0000")

        # Максимальное значение
        gen_max = card_number_generator(9999_9999_9999_9999, 9999_9999_9999_9999)
        self.assertEqual(next(gen_max), "9999 9999 9999 9999")

    def test_lazy_evaluation(self):
        """Тест ленивой оценки генератора"""
        gen = card_number_generator(1, 10_000)
        first = next(gen)
        self.assertEqual(first, "0000 0000 0000 0001")
        second = next(gen)
        self.assertEqual(second, "0000 0000 0000 0002")


if __name__ == '__main__':
    unittest.main()
