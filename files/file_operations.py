import csv

import pandas as pd


def read_transactions_from_csv(file_path: str):
    transactions = []

    # Увеличиваем лимит для полей
    csv.field_size_limit(1000000)  # Установите лимит на 1 миллион символов

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(row)
    return transactions


# Пример использования функции
file_path = '/home/ira/10.1/files/transactions.csv'
transactions = read_transactions_from_csv(file_path)
print(transactions)


def read_transactions_from_excel(file_path: str):
    """
    Читает финансовые операции из Excel-файла.

    :param file_path: Путь к Excel-файлу.
    :return: Список словарей с транзакциями.
    """
    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path, engine='openpyxl')  # Указываем движок для чтения
        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict(orient='records')
        return transactions
    except ValueError as e:
        print(f"Ошибка при чтении файла Excel: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


# Пример использования функции
file_path = '/home/ira/10.1/files/transactions_excel.xlsx'
transactions = read_transactions_from_excel(file_path)
print(transactions)
