import unittest
import csv
import openpyxl
import os
from tempfile import NamedTemporaryFile
from unittest.mock import patch
from src.reading_from_tabs import read_financial_transactions, read_csv, read_xlsx


class TestFinancialTransactionsReader(unittest.TestCase):
    def setUp(self):
        """Создаем временные файлы для тестов"""
        # Создаем временный CSV файл
        self.csv_data = [
            {"date": "2023-01-01", "description": "Salary", "amount": "1000.00"},
            {"date": "2023-01-02", "description": "Rent", "amount": "-500.50"}
        ]
        self.csv_file = NamedTemporaryFile(mode='w+', suffix='.csv', delete=False)
        writer = csv.DictWriter(self.csv_file, fieldnames=["date", "description", "amount"])
        writer.writeheader()
        writer.writerows(self.csv_data)
        self.csv_file.close()

        # Создаем временный XLSX файл
        self.xlsx_file = NamedTemporaryFile(suffix='.xlsx', delete=False)
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["date", "description", "amount"])  # Заголовки
        sheet.append(["2023-01-01", "Salary", 1000.00])
        sheet.append(["2023-01-02", "Rent", -500.50])
        workbook.save(self.xlsx_file.name)
        workbook.close()
        self.xlsx_file.close()

    def tearDown(self):
        """Удаляем временные файлы после тестов"""
        os.unlink(self.csv_file.name)
        os.unlink(self.xlsx_file.name)

    def test_read_csv_valid_file(self):
        """Тест чтения корректного CSV файла"""
        result = read_csv(self.csv_file.name)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["description"], "Salary")
        self.assertAlmostEqual(float(result[0]["amount"]), 1000.00)
        self.assertEqual(result[1]["date"], "2023-01-02")

    def test_read_xlsx_valid_file(self):
        """Тест чтения корректного XLSX файла"""
        result = read_xlsx(self.xlsx_file.name)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["description"], "Salary")
        self.assertAlmostEqual(result[0]["amount"], 1000.00)
        self.assertEqual(result[1]["date"], "2023-01-02")

    def test_read_financial_transactions_csv(self):
        """Тест автоматического определения CSV формата"""
        result = read_financial_transactions(self.csv_file.name)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["description"], "Salary")

    def test_read_financial_transactions_xlsx(self):
        """Тест автоматического определения XLSX формата"""
        result = read_financial_transactions(self.xlsx_file.name)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["description"], "Rent")

    def test_amount_conversion_csv(self):
        """Тест конвертации суммы в CSV"""
        result = read_csv(self.csv_file.name)
        self.assertIsInstance(result[0]["amount"], float)
        self.assertIsInstance(result[1]["amount"], float)

    def test_amount_conversion_xlsx(self):
        """Тест конвертации суммы в XLSX"""
        result = read_xlsx(self.xlsx_file.name)
        self.assertIsInstance(result[0]["amount"], float)
        self.assertIsInstance(result[1]["amount"], float)

    def test_read_csv_missing_file(self):
        """Тест обработки отсутствующего CSV файла"""
        with self.assertRaises(FileNotFoundError):
            read_csv("nonexistent.csv")

    def test_read_xlsx_missing_file(self):
        """Тест обработки отсутствующего XLSX файла"""
        with self.assertRaises(FileNotFoundError):
            read_xlsx("nonexistent.xlsx")

    def test_read_unsupported_format(self):
        """Тест обработки неподдерживаемого формата файла"""
        with self.assertRaises(ValueError):
            read_financial_transactions("test.txt")

    def test_read_csv_with_different_headers(self):
        """Тест чтения CSV с разными названиями столбцов"""
        # Создаем временный файл с другими заголовками
        with NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as temp_file:
            writer = csv.DictWriter(temp_file, fieldnames=["date", "описание", "сумма"])
            writer.writeheader()
            writer.writerow({"date": "2023-01-03", "описание": "Продукты", "сумма": "150.75"})
            temp_file.close()

            result = read_csv(temp_file.name)
            os.unlink(temp_file.name)

            self.assertEqual(len(result), 1)
            self.assertAlmostEqual(result[0]["сумма"], 150.75)

    def test_read_empty_csv(self):
        """Тест чтения пустого CSV файла"""
        with NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as temp_file:
            temp_file.write("date,description,amount\n")
            temp_file.close()

            result = read_csv(temp_file.name)
            os.unlink(temp_file.name)

            self.assertEqual(len(result), 0)

    def test_read_empty_xlsx(self):
        """Тест чтения пустого XLSX файла (только заголовки)"""
        temp_file = NamedTemporaryFile(suffix='.xlsx', delete=False)
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["date", "description", "amount"])  # Только заголовки
        workbook.save(temp_file.name)
        workbook.close()
        temp_file.close()

        result = read_xlsx(temp_file.name)
        os.unlink(temp_file.name)

        self.assertEqual(len(result), 0)

    @patch('finance_reader.openpyxl.load_workbook')
    def test_xlsx_read_error(self, mock_load):
        """Тест обработки ошибки чтения XLSX"""
        mock_load.side_effect = Exception("Test error")
        with self.assertRaises(Exception):
            read_xlsx(self.xlsx_file.name)

    def test_csv_with_missing_values(self):
        """Тест обработки отсутствующих значений в CSV"""
        with NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as temp_file:
            writer = csv.DictWriter(temp_file, fieldnames=["date", "description", "amount"])
            writer.writeheader()
            writer.writerow({"date": "2023-01-04", "description": "", "amount": "200"})
            writer.writerow({"date": "2023-01-05", "description": "Bonus", "amount": ""})
            temp_file.close()

            result = read_csv(temp_file.name)
            os.unlink(temp_file.name)

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["description"], "")
            self.assertIsNone(result[1].get("amount"))


if __name__ == '__main__':
    unittest.main()
