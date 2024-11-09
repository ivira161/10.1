from typing import Dict, List


def filter_by_state(dict_user: List[Dict[str, str]], state: str = 'EXECUTED') -> List[Dict[str, str]]:
    '''Функция, которая принимает список словарей и опционально значение для ключа state
    (по умолчанию 'EXECUTED'). Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state, соответствует указанному значению.'''
    filtered_list = [user for user in dict_user if user.get('state') == 'EXECUTED']
    return filtered_list


def sort_by_date(data: List[Dict], order: str = 'desc') -> List[Dict]:
    ''' Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция должна возвращать новый список, отсортированный по дате (date).'''
    # Определяем, следует ли сортировать по убыванию или возрастанию
    if order == 'desc':
        reverse = True  # Сортировка по убыванию
    else:
        reverse = False  # Сортировка по возрастанию

    # Используем функцию sorted для сортировки данных
    # Указываем, что нужно сортировать по ключу 'date'
    sorted_data = sorted(data, key=lambda x: x['date'], reverse=reverse)

    return sorted_data
