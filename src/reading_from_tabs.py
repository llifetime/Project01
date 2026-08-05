from pathlib import Path
from typing import Dict, List

import pandas as pd
import openpyxl
import csv


def read_financial_transactions(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из файла (CSV или XLSX) с помощью pandas

    Параметры:
        file_path (str): Путь к файлу с транзакциями

    Возвращает:
        List[Dict]: Список словарей с транзакциями

    Исключения:
        ValueError: Если формат файла не поддерживается
        FileNotFoundError: Если файл не существует
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    file_ext = file_path.suffix.lower()

    try:
        if file_ext == '.csv':
            df = pd.read_csv(file_path)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {file_ext}")

        # Конвертируем DataFrame в список словарей
        transactions = df.replace({pd.NA: None}).to_dict('records')

        # Автоматически определяем поля с суммами для конвертации
        amount_fields = [col for col in df.columns if col.lower() in ['amount', 'sum', 'сумма']]

        for transaction in transactions:
            for field in amount_fields:
                if field in transaction and transaction[field] is not None:
                    try:
                        transaction[field] = float(transaction[field])
                    except (ValueError, TypeError):
                        pass

        return transactions

    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла {file_path}: {str(e)}")


# Пример использования
if __name__ == "__main__":
    try:
        # Чтение из CSV
        csv_transactions = read_financial_transactions("transactions.csv")
        print(f"Прочитано {len(csv_transactions)} транзакций из CSV:")
        print(csv_transactions[:2])  # Выводим первые 2 транзакции для примера

        # Чтение из XLSX
        xlsx_transactions = read_financial_transactions("transactions.xlsx")
        print(f"\nПрочитано {len(xlsx_transactions)} транзакций из XLSX:")
        print(xlsx_transactions[:2])

    except Exception as e:
        print(f"Ошибка: {e}")


def read_csv(file_path: str) -> List[Dict]:
    """Читает данные из CSV файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []


def read_xlsx(file_path: str) -> List[Dict]:
    """Читает данные из XLSX файла."""
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1] if cell.value]
        transactions = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = {}
            for i, value in enumerate(row):
                if i < len(headers) and headers[i]:
                    row_data[headers[i]] = value
            if row_data:  # Добавляем только непустые строки
                transactions.append(row_data)

        return transactions
    except FileNotFoundError:
        return []
    except Exception:
        return []


def read_file(file_path: str, file_type: str = None) -> List[Dict]:
    """
    Читает файл автоматически определяя тип или по указанному типу.

    Args:
        file_path: Путь к файлу
        file_type: Тип файла ('json', 'csv', 'xlsx'). Если None, определяется по расширению.

    Returns:
        List[Dict]: Список транзакций
    """
    if file_type is None:
        # Автоматическое определение по расширению
        if file_path.lower().endswith('.csv'):
            return read_csv(file_path)
        elif file_path.lower().endswith(('.xlsx', '.xls')):
            return read_xlsx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    else:
        # Чтение по указанному типу
        file_type = file_type.lower()
        if file_type == 'csv':
            return read_csv(file_path)
        elif file_type in ('xlsx', 'xls'):
            return read_xlsx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
