import re
from typing import Dict, List


def filter_operations_by_description(operations, search_string):
    """
    Фильтрует список операций, оставляя только те, в описании которых есть искомая строка.

    Args:
        operations: Список словарей с данными о банковских операциях.
        search_string: Строка для поиска в описании операции (регистронезависимо).

    Returns:
        Список словарей, у которых в поле 'description' найдена искомая строка.
    """
    if not search_string:
        return operations

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    filtered_operations = [
        op for op in operations
        if op.get('description') and pattern.search(op['description'])
    ]

    return filtered_operations


def count_operations_by_category(operations: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций для каждой заданной категории.

    Args:
        operations: Список словарей с данными о банковских операциях.
        categories: Список категорий для поиска в поле 'description'.

    Returns:
        Словарь, где ключи — категории, а значения — количество операций.
        Если категория не найдена ни в одной операции, её значение будет 0.
    """
    category_counts = {category: 0 for category in categories}

    for operation in operations:
        description = operation.get('description', '').lower()
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1

    return category_counts
