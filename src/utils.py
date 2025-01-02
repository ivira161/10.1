import json
import os
import re
import pandas as pd
from collections import Counter
from typing import List, Dict, Any
import openpyxl

# Определяем базовую директорию как директорию самого файла utils.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")


def read_csv_transactions(csv_filename: str = "transactions.csv"):
    """
    Считывает финансовые операции из CSV-файла (pandas) и возвращает список словарей.
    :param csv_filename: имя CSV-файла (по умолчанию 'transactions.csv')
    :return: список словарей с данными.
    """
    file_path = os.path.join(DATA_DIR, csv_filename)
    try:
        df = pd.read_csv(file_path, sep=";", encoding="utf-8")
        # Превращаем DataFrame в список словарей
        return df.to_dict(orient="records")
    except FileNotFoundError:
        return []
    except pd.errors.EmptyDataError:
        # Файл пуст
        return []
    except Exception:
        # На случай других ошибок (ошибочные заголовки, кодировка и т.д.)
        return []


def read_json_transactions(json_filename: str = "operations.json"):
    """
    Считывает финансовые операции из JSON-файла через стандартный json-модуль
    и возвращает список словарей. Если файл не найден, пустой или содержит не список, возвращаем пустой список.
    :param json_filename: имя JSON-файла (по умолчанию 'operations.json')
    :return: список словарей
    """
    file_path = os.path.join(DATA_DIR, json_filename)
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def read_excel_transactions(excel_filename: str = "transactions_excel.xlsx"):
    """
    Считывает финансовые операции из Excel (через openpyxl) и возвращает список словарей.

    Предполагаем, что:
    1) Первая строка в Excel — заголовки столбцов.
    2) Каждый последующий ряд — данные для транзакции.

    :param excel_filename: имя Excel-файла (по умолчанию 'transactions_excel.xlsx')
    :return: список словарей вида [{header1: value1, header2: value2, ...}, ...]
    """
    file_path = os.path.join(DATA_DIR, excel_filename)
    try:
        # Загружаем книгу в режиме чтения
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = wb.active  # Используем первый (активный) лист
        rows = list(sheet.rows)
        if not rows:
            return []

        # Первая строка — заголовки
        headers = [cell.value for cell in rows[0]]
        transactions = []

        # Начиная со второй строки — данные
        for row in rows[1:]:
            row_values = [cell.value for cell in row]
            # Превращаем в словарь: {header: value}
            transaction_dict = dict(zip(headers, row_values))
            transactions.append(transaction_dict)

        return transactions
    except FileNotFoundError:
        # Файл не найден — вернём пустой список
        return []
    except Exception:
        # Любая другая ошибка при чтении (битый Excel и т.д.) — тоже пустой список
        return []


def search_transactions(transactions: list[dict[str, any]], search_str: str) -> list[dict[str, any]]:
    """
    Ищет все операции, в поле 'description' которых встречается подстрока search_str
    (с использованием регулярных выражений).

    :param transactions: список словарей с операциями
    :param search_str: строка поиска
    :return: список словарей, подходящих под условие
    """
    result = []
    pattern = re.compile(re.escape(search_str), re.IGNORECASE)
    for txn in transactions:
        description = txn.get('description', '') or ''
        if pattern.search(description):
            result.append(txn)
    return result


def count_categories(transactions: list[dict[str, any]], categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество операций в каждой категории (categories),
    сравнивая каждую категорию с полем 'description'.

    :param transactions: список с транзакциями
    :param categories: список категорий (строк), которые нужно искать
    :return: словарь, где ключи - это категории, а значения - количество операций
    """
    # Можно применить Counter, но придётся пройтись по операциям и проверять описание
    # Например, если в description есть точное вхождение категории, считаем это совпадением
    counter = Counter()
    for txn in transactions:
        desc = txn.get('description', '') or ''
        for cat in categories:
            # Предположим, что мы ищем точное вхождение категории в описании
            # (Например, re.search(fr"\b{re.escape(cat)}\b", desc, re.IGNORECASE))
            if cat.lower() in desc.lower():
                counter[cat] += 1
    # Превратим Counter обратно в обычный dict
    result = dict(counter)
    return result