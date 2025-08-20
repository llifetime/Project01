import csv
import json
from datetime import datetime
from typing import Dict, List, Optional

import openpyxl

from src.masks import get_mask_account, get_mask_card_number
from src.widget import get_date, mask_card


def load_json_transactions(file_path: str) -> List[Dict]:
    """Загружает транзакции из JSON-файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_csv_transactions(file_path: str) -> List[Dict]:
    """Загружает транзакции из CSV-файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []


def load_xlsx_transactions(file_path: str) -> List[Dict]:
    """Загружает транзакции из XLSX-файла"""
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]
        transactions = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            transactions.append(dict(zip(headers, row)))

        return transactions
    except FileNotFoundError:
        return []


def filter_by_status(transactions: List[Dict], status: str) -> List[Dict]:
    """Фильтрует транзакции по статусу (без учета регистра)"""
    return [t for t in transactions
            if t.get('status', '').upper() == status.upper()]


def sort_transactions(transactions: List[Dict], reverse: bool = False) -> List[Dict]:
    """Сортирует транзакции по дате"""
    return sorted(transactions,
                  key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'),
                  reverse=reverse)


def filter_rub_only(transactions: List[Dict]) -> List[Dict]:
    """Фильтрует только рублевые транзакции"""
    return [t for t in transactions
            if t.get('currency', '').upper() == 'RUB']


def filter_by_description(transactions: List[Dict], keyword: str) -> List[Dict]:
    """Фильтрует транзакции по ключевому слову в описании"""
    return [t for t in transactions
            if keyword.lower() in t.get('description', '').lower()]


def format_transaction(transaction: Dict) -> str:
    """Форматирует транзакцию для вывода"""
    date = transaction.get('date', '')
    description = transaction.get('description', '')
    amount = transaction.get('amount', '')
    currency = transaction.get('currency', '').upper()

    if '->' in description:
        parts = description.split('->')
        from_account = parts[0].strip()
        to_account = parts[1].strip()
        account_info = f"{from_account} -> {to_account}"
    else:
        account_info = f"Счет **{transaction.get('account', '')[-4:]}"

    return (f"{date} {description}\n"
            f"{account_info}\n"
            f"Сумма: {amount} {currency}\n")


def get_user_input(prompt: str, options: Optional[List[str]] = None) -> str:
    """Получает ввод пользователя с валидацией"""
    while True:
        user_input = input(prompt).strip()
        if not options or user_input.lower() in [o.lower() for o in options]:
            return user_input
        print(f"Некорректный ввод. Допустимые варианты: {', '.join(options)}")


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_type = get_user_input("Ваш выбор (1-3): ", ["1", "2", "3"])
    file_path = input("Введите путь к файлу: ")

    if file_type == "1":
        transactions = load_json_transactions(file_path)
        print("\nДля обработки выбран JSON-файл.")
    elif file_type == "2":
        transactions = load_csv_transactions(file_path)
        print("\nДля обработки выбран CSV-файл.")
    else:
        transactions = load_xlsx_transactions(file_path)
        print("\nДля обработки выбран XLSX-файл.")

    if not transactions:
        print("Не удалось загрузить транзакции. Проверьте путь к файлу.")
        return

    # Фильтрация по статусу
    print("\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
    while True:
        status = input("Введите статус, по которому необходимо выполнить фильтрацию: ").upper()
        if status in ["EXECUTED", "CANCELED", "PENDING"]:
            break
        print(f'Статус операции "{status}" недоступен.')

    filtered = filter_by_status(transactions, status)
    print(f'\nОперации отфильтрованы по статусу "{status}"')

    if not filtered:
        print("Не найдено ни одной транзакции с указанным статусом.")
        return

    # Сортировка
    sort_choice = get_user_input("Отсортировать операции по дате? (Да/Нет): ", ["да", "нет"])
    if sort_choice.lower() == "да":
        order_choice = get_user_input("Отсортировать по возрастанию или по убыванию? ",
                                      ["по возрастанию", "по убыванию"])
        filtered = sort_transactions(filtered, reverse=order_choice.lower() == "по убыванию")

    # Фильтрация по валюте
    rub_choice = get_user_input("Выводить только рублевые транзакции? (Да/Нет): ", ["да", "нет"])
    if rub_choice.lower() == "да":
        filtered = filter_rub_only(filtered)

    # Фильтрация по описанию
    desc_choice = get_user_input("Отфильтровать список транзакций по определенному слову в описании? (Да/Нет): ",
                                 ["да", "нет"])
    if desc_choice.lower() == "да":
        keyword = input("Введите слово для поиска в описании: ")
        filtered = filter_by_description(filtered, keyword)

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(filtered)}\n")

    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        for transaction in filtered:
            print(format_transaction(transaction))


if __name__ == "__main__":
    main()
    print(get_mask_card_number("73654108430135874305"))
    print(get_mask_account("73654108430135874305"))
    print(mask_card("Счет 187893747174714974"))
    print(get_date("2024-03-11T02:26:18.671407"))
