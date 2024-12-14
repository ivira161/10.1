import json
import logging
import os
import csv
import pandas as pd


# Создаем папку logs, если она не существует
if not os.path.exists('logs'):
    os.makedirs('logs')

# Настройка логирования
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logs/utils.log')
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

# Примеры логирования
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')


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
        logger.error(f"Файл не найден: {absolute_path}")
        return []

    with open(absolute_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                logger.info("Успешно прочитаны данные из JSON.")
                return data
            else:
                logger.warning("Содержимое файла не является списком.")
                return []
        except json.JSONDecodeError:
            logger.error("Ошибка декодирования JSON.")
            return []


# Пример использования функции
file_path = 'operations.json'  # Относительный путь к файлу
transactions = read_transactions_from_json(file_path)
print(transactions)


def read_transactions_from_csv(file_path: str):
    transactions = []

    # Увеличиваем лимит для полей
    csv.field_size_limit(1000000)  # Установите лимит на 1 миллион символов

    # Добавлено: Проверка существования файла перед открытием
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(row)
    return transactions

# Пример использования функции
file_path = '/home/ira/10.1/data/transactions.csv'
transactions = read_transactions_from_csv(file_path)
print(transactions)


def read_transactions_from_excel(file_path: str):
    """
    Читает финансовые операции из Excel-файла.

    :param file_path: Путь к Excel-файлу.
    :return: Список словарей с транзакциями.
    """
    # Добавлено: Проверка существования файла перед открытием
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

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
file_path = '/home/ira/10.1/data/transactions_excel.xlsx'
transactions = read_transactions_from_excel(file_path)
print(transactions)

