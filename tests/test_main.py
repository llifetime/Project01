"""Тесты для основного модуля main.py."""

import unittest
from unittest.mock import patch
import io

from main import get_user_input, main, format_transaction


class TestMainModule(unittest.TestCase):

    def test_get_user_input_valid(self):
        """Тест корректного ввода пользователя."""
        with patch('builtins.input', return_value='да'):
            result = get_user_input("Тест: ", ["да", "нет"])
            self.assertEqual(result, "да")

    def test_get_user_input_case_insensitive(self):
        """Тест ввода в разном регистре."""
        with patch('builtins.input', return_value='ДА'):
            result = get_user_input("Тест: ", ["да", "нет"])
            self.assertEqual(result, "ДА")

    def test_get_user_input_retry(self):
        """Тест повторного ввода при ошибке."""
        with patch('builtins.input', side_effect=['неверно', 'да']):
            with patch('builtins.print') as mock_print:
                result = get_user_input("Тест: ", ["да", "нет"])
                self.assertEqual(result, "да")
                mock_print.assert_called_once()

    def test_format_transaction_basic(self):
        """Тест форматирования базовой транзакции."""
        transaction = {
            'date': '01.01.2023',
            'description': 'Перевод',
            'amount': '100',
            'currency': 'RUB',
            'account': '1234567890'
        }
        result = format_transaction(transaction)
        self.assertIn('01.01.2023 Перевод', result)
        self.assertIn('Счет **7890', result)
        self.assertIn('100 RUB', result)

    def test_format_transaction_with_arrow(self):
        """Тест форматирования транзакции с переводом."""
        transaction = {
            'date': '01.01.2023',
            'description': 'Карта 1234 -> Карта 5678',
            'amount': '200',
            'currency': 'USD'
        }
        result = format_transaction(transaction)
        self.assertIn('Карта 1234 -> Карта 5678', result)

    @patch('src.main.load_json_transactions')
    @patch('builtins.input')
    @patch('sys.exit')
    def test_main_json_success_flow(self, mock_exit, mock_input, mock_load):
        """Тест успешного выполнения с JSON файлом."""
        # Настройка моков
        mock_input.side_effect = [
            '1',  # Выбор JSON
            'data/transactions.json',  # Путь к файлу
            'EXECUTED',  # Статус
            'нет',  # Сортировка
            'нет',  # RUB only
            'нет'  # Фильтр по описанию
        ]

        mock_load.return_value = [{
            'date': '01.01.2023',
            'status': 'EXECUTED',
            'amount': '100',
            'currency': 'RUB',
            'description': 'Тест'
        }]

        # Захват вывода
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()

        # Проверки
        mock_load.assert_called_once_with('data/transactions.json')
        output = mock_stdout.getvalue()
        self.assertIn('Для обработки выбран JSON-файл', output)
        self.assertIn('EXECUTED', output)

    @patch('src.main.load_json_transactions')
    @patch('builtins.input')
    @patch('sys.exit')
    def test_main_empty_transactions(self, mock_exit, mock_input, mock_load):
        """Тест обработки пустого файла."""
        mock_input.side_effect = ['1', 'empty.json']
        mock_load.return_value = []

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()

        output = mock_stdout.getvalue()
        self.assertIn('Не удалось загрузить транзакции', output)
        mock_exit.assert_called_once_with(1)

    @patch('src.main.load_json_transactions')
    @patch('builtins.input')
    @patch('sys.exit')
    def test_main_no_matching_status(self, mock_exit, mock_input, mock_load):
        """Тест отсутствия транзакций с нужным статусом."""
        mock_input.side_effect = [
            '1', 'data/file.json',
            'EXECUTED'  # Статус, которого нет в данных
        ]

        mock_load.return_value = [{
            'date': '01.01.2023',
            'status': 'CANCELED',  # Другой статус
            'amount': '100',
            'currency': 'RUB'
        }]

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()

        output = mock_stdout.getvalue()
        self.assertIn('Не найдено ни одной транзакции', output)
        mock_exit.assert_called_once_with(0)

    @patch('src.main.load_json_transactions')
    @patch('builtins.input')
    @patch('sys.exit')
    def test_main_invalid_status_retry(self, mock_exit, mock_input, mock_load):
        """Тест повторного ввода статуса."""
        mock_input.side_effect = [
            '1', 'data/file.json',
            'INVALID',  # Неверный статус
            'EXECUTED',  # Верный статус
            'нет', 'нет', 'нет'
        ]

        mock_load.return_value = [{
            'date': '01.01.2023',
            'status': 'EXECUTED',
            'amount': '100',
            'currency': 'RUB'
        }]

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()

        output = mock_stdout.getvalue()
        self.assertIn('недоступен', output)  # Сообщение об ошибке статуса
        self.assertIn('EXECUTED', output)  # Успешная фильтрация

    @patch('src.main.load_csv_transactions')
    @patch('builtins.input')
    @patch('sys.exit')
    def test_main_csv_file(self, mock_exit, mock_input, mock_load):
        """Тест работы с CSV файлом."""
        mock_input.side_effect = [
            '2', 'data/transactions.csv',
            'EXECUTED', 'нет', 'нет', 'нет'
        ]

        mock_load.return_value = [{
            'date': '01.01.2023',
            'status': 'EXECUTED',
            'amount': '100',
            'currency': 'RUB'
        }]

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()

        output = mock_stdout.getvalue()
        self.assertIn('CSV-файл', output)

    @patch('src.main.load_xlsx_transactions')
    @patch('builtins.input')
    @patch('sys.exit')
    def test_main_xlsx_file(self, mock_exit, mock_input, mock_load):
        """Тест работы с XLSX файлом."""
        mock_input.side_effect = [
            '3', 'data/transactions.xlsx',
            'EXECUTED', 'нет', 'нет', 'нет'
        ]

        mock_load.return_value = [{
            'date': '01.01.2023',
            'status': 'EXECUTED',
            'amount': '100',
            'currency': 'RUB'
        }]

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()

        output = mock_stdout.getvalue()
        self.assertIn('XLSX-файл', output)


if __name__ == '__main__':
    unittest.main()
