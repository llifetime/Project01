from pathlib import Path
from typing import Dict, List

import pandas as pd


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
