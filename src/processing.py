def filter_by_state(list_of_dict: list, state: str = 'EXECUTED') -> list:

    '''Функция для фильтрации по признаку выполнения опецрации.'''

    filtered_list = []
    for dict_ in list_of_dict:
        if dict_.get('state') == state:
            filtered_list.append(dict_)
        else:
            continue

    return filtered_list


result = filter_by_state(list_of_dict=eval(input("Enter the list of dictionaries: ")))


print(result)


def sort_by_date(list_of_dict: list, rev: bool = True) -> list:

    ''' Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание). Функция должна возвращать
     новый список, отсортированный по дате (date).'''

    sorted_list_of_date = sorted(list_of_dict, key=lambda dict_: dict_["date"], reverse=rev)
    return sorted_list_of_date
