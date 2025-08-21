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

    def convert_to_float(value):
        try:
            return float(value) if value is not None else None
        except (ValueError, TypeError):
            return None

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

if __name__ == '__main__':
    unittest.main()
