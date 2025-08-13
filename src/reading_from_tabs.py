import csv
import openpyxl
from typing import List, Dict
from pathlib import Path


def read_financial_transactions(file_path: str) -> List[Dict]:
    """
    Чтение финансовых операций из файла (CSV или XLSX)

    :param file_path: Путь к файлу
    :return: Список словарей с транзакциями
    """
    file_ext = Path(file_path).suffix.lower()

    if file_ext == '.csv':
        return read_csv(file_path)
    elif file_ext == '.xlsx':
        return read_xlsx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")


def read_csv(file_path: str) -> List[Dict]:
    """
    Чтение финансовых операций из CSV файла

    :param file_path: Путь к CSV файлу
    :return: Список словарей с транзакциями
    """
    transactions = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Преобразуем числовые значения при наличии
            processed_row = {}
            for key, value in row.items():
                if key.lower() in ['amount', 'sum', 'сумма'] and value:
                    try:
                        processed_row[key] = float(value)
                    except ValueError:
                        processed_row[key] = value
                else:
                    processed_row[key] = value

            transactions.append(processed_row)

    return transactions


def read_xlsx(file_path: str) -> List[Dict]:
    """
    Чтение финансовых операций из XLSX файла

    :param file_path: Путь к XLSX файлу
    :return: Список словарей с транзакциями
    """
    transactions = []

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Получаем заголовки из первой строки
    headers = []
    for cell in sheet[1]:
        headers.append(cell.value)

    # Читаем остальные строки
    for row in sheet.iter_rows(min_row=2, values_only=True):
        transaction = {}

        for i, value in enumerate(row):
            header = headers[i] if i < len(headers) else f"Column_{i + 1}"

            if header and header.lower() in ['amount', 'sum', 'сумма'] and value is not None:
                try:
                    transaction[header] = float(value)
                except (ValueError, TypeError):
                    transaction[header] = value
            else:
                if header:  # Игнорируем колонки без заголовка
                    transaction[header] = value

        transactions.append(transaction)

    return transactions


def main():
    try:
        # Чтение из CSV файла
        csv_file = 'transactions.csv'
        if Path(csv_file).exists():
            csv_transactions = read_financial_transactions(csv_file)
            print(f"Успешно прочитано {len(csv_transactions)} операций из {csv_file}")
            print("Первые 2 операции:")
            for op in csv_transactions[:2]:
                print(op)
        else:
            print(f"Файл {csv_file} не найден")

        print("\n" + "=" * 50 + "\n")

        # Чтение из XLSX файла
        xlsx_file = 'transactions_excel.xlsx'
        if Path(xlsx_file).exists():
            xlsx_transactions = read_financial_transactions(xlsx_file)
            print(f"Успешно прочитано {len(xlsx_transactions)} операций из {xlsx_file}")
            print("Первые 2 операции:")
            for op in xlsx_transactions[:2]:
                print(op)
        else:
            print(f"Файл {xlsx_file} не найден")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
