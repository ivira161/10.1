import json
import os


def read_transactions_from_json(file_path: str):
    """
    Читает транзакции из JSON-файла.

    :param file_path: Путь к JSON-файлу.
    :return: Список словарей с данными о финансовых транзакциях.
    """
    # Получаем абсолютный путь к файлу
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = os.path.join(BASE_DIR, "data", file_path)

    if not os.path.exists(absolute_path):
        print(f"Файл не найден: {absolute_path}")
        return []

    with open(absolute_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print("Содержимое файла не является списком.")
                return []
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON.")
            return []


# Пример использования функции
file_path = 'operations.json'  # Относительный путь к файлу
transactions = read_transactions_from_json(file_path)
print(transactions)
