from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(dict_user: List[Dict[str, str]], state: str = 'EXECUTED') -> List[Dict[str, str]]:
    '''
    Функция, которая принимает список словарей и опционально значение для ключа state
    (по умолчанию 'EXECUTED'). Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению.
    '''
    if not dict_user:  # Проверка на пустой список
        return []  # Возвращаем пустой список, если список пуст
    # Изменено: теперь используем переданный параметр state
    filtered_list = [user for user in dict_user if user.get('state') == state]

    return filtered_list


def sort_by_date(data: List[Dict[str, Any]], order: str = 'desc') -> List[Dict[str, Any]]:
    '''
    Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате (date).
    '''
    reverse = (order == 'desc')  # Если order 'desc', то сортировка по убыванию

    # Проверка формата даты
    for item in data:
        try:
            item['date'] = datetime.strptime(item['date'], '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Некорректный формат даты: {item['date']}")

    # Используем функцию sorted для сортировки данных
    sorted_data = sorted(data, key=lambda x: x['date'], reverse=reverse)
    return sorted_data
