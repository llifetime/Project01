import json
import os
from typing import List, Dict
from external_api import convert_currency


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    :param file_path: Путь до JSON-файла (например, '.src/operations.json')
    :return: Список словарей с транзакциями. Если файл не найден, пуст или невалиден — возвращает [].
    """
    try:
        # Преобразуем путь в абсолютный (если он относительный)
        abs_path = os.path.abspath(file_path)

        with open(abs_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if isinstance(data, list):
                # Проверяем, что все элементы — словари (если список не пуст)
                if data and all(isinstance(item, dict) for item in data):
                    return data
                return []  # если список пуст или содержит не словари
            return []  # если JSON не список

    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
        return []  # если файл не найден, битый JSON или ошибка кодировки


def get_transaction_amount_in_rub(transaction: Dict) -> float:
        """
        Возвращает сумму транзакции в рублях (float).
        Если валюта — USD или EUR, конвертирует по текущему курсу.

        :param transaction: Словарь с данными транзакции
        :return: Сумма в рублях (float)
        :raises: ValueError, если транзакция некорректна или API недоступно
        """
        if not isinstance(transaction, dict):
            raise ValueError("Transaction must be a dictionary")

        amount = transaction.get('amount')
        currency = transaction.get('currency', 'RUB').upper()

        if amount is None:
            raise ValueError("Transaction is missing 'amount'")

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Amount must be a number")

        if currency == 'RUB':
            return amount
        elif currency in ('USD', 'EUR'):
            return convert_currency(amount, currency)
        else:
            raise ValueError(f"Unsupported currency: {currency}")