
filtered_list = []


def filter_by_state(list_of_dict: list, state='EXECUTED') -> list:
    for dict in list_of_dict:
        if dict.get('state') == state:
            filtered_list.append(dict)
        else:
            continue

    return filtered_list


result = filter_by_state(list_of_dict=eval(input("Enter the list of dictionaries: ")))

print(result)


def sort_by_date(list_of_dict: list, decreasing: bool = True) -> list:

    ''' Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание). Функция должна возвращать
     новый список, отсортированный по дате (date).'''

    sorted_by_date = sorted(list_of_dict, key=lambda x: int(x['date'].split('T')[0].replace('-', '')), reverse=decreasing)
    return sorted_by_date
