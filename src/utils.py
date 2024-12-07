import json
import os

from src.external_api import convert_to_rub

def read_transactions_from_json(file_path: str):
    """
    Читает транзакции из JSON-файла.

    :param file_path: Путь к JSON-файлу.
    :return: Список словарей с данными о финансовых транзакциях.
    """
    # Получаем абсолютный путь к файлу
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = os.path.join(BASE_DIR, "data", file_path)  # Исправлено

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



def read_transactions_from_json(file_path: str):
    """
    Читает транзакции из JSON-файла.

    :param file_path: Путь к JSON-файлу.
    :return: Список словарей с данными о финансовых транзакциях.
    """
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return []

    with open(file_path, 'r', encoding='utf-8') as file:
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


def calculate_transaction_amount(transaction: dict) -> float:
    """
    Рассчитывает сумму транзакции в рублях.

    :param transaction: Словарь с данными о транзакции.
    :return: Сумма транзакции в рублях.
    """
    amount = transaction.get('amount', 0.0)
    currency = transaction.get('currency', 'RUB')

    if amount < 0:
        return amount  # Возвращаем отрицательную сумму без конвертации

    return convert_to_rub(amount, currency)