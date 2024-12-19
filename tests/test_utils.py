import unittest
import pytest
from unittest.mock import mock_open, patch
import pandas as pd
import csv
import os
from src.utils import read_transactions_from_json, read_transactions_from_csv, read_transactions_from_excel
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data') # Директория с тестовыми данными


class TestReadTransactionsFromJson(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "amount": 100, "currency": "USD"}]')
    @patch("os.path.exists", return_value=True)
    def test_valid_json(self, mock_exists, mock_file):
        result = read_transactions_from_json('data/operations.json')
        expected = [{"id": 1, "amount": 100, "currency": "USD"}]
        self.assertEqual(result, expected)  # Ожидаем, что вернется корректный список

    @patch("builtins.open", new_callable=mock_open, read_data='not a json')
    @patch("os.path.exists", return_value=True)
    def test_invalid_json(self, mock_exists, mock_file):
        result = read_transactions_from_json('data/invalid.json')
        self.assertEqual(result, [])  # Ожидаем пустой список

    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    @patch("os.path.exists", return_value=True)
    def test_empty_json(self, mock_exists, mock_file):
        result = read_transactions_from_json('data/empty.json')
        self.assertEqual(result, [])  # Ожидаем пустой список

    @patch("os.path.exists", return_value=False)
    def test_file_not_found(self, mock_exists):
        result = read_transactions_from_json('data/non_existent_file.json')
        self.assertEqual(result, [])  # Ожидаем пустой список

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    @patch("os.path.exists", return_value=True)
    def test_json_not_a_list(self, mock_exists, mock_file):
        result = read_transactions_from_json('data/invalid_list.json')
        self.assertEqual(result, [])  # Ожидаем пустой список



@patch("builtins.open", new_callable=mock_open, read_data='Name;Amount;Currency\nAlice;100;RUB\nBob;200;USD')
@patch("os.path.exists", return_value=True) # Добавлена эта строка
def test_read_transactions_from_csv(mock_exists, mock_file): # Изменено для mock_exists
    file_path = 'dummy.csv'
    expected_result = [
        {'Name': 'Alice', 'Amount': '100', 'Currency': 'RUB'},
        {'Name': 'Bob', 'Amount': '200', 'Currency': 'USD'}
    ]
    result = read_transactions_from_csv(file_path)
    assert result == expected_result

@patch("os.path.exists", return_value=False)
def test_read_transactions_from_csv_file_not_found(mock_exists):
    result = read_transactions_from_csv('non_existent_file.csv')
    assert result == []

# Тест для функции считывания из Excel
@patch('pandas.read_excel')
@patch("os.path.exists", return_value=True) # Добавлена эта строка
def test_read_transactions_from_excel(mock_exists,mock_read_excel):
    # ВАЖНО:  Указываем, что mock_read_excel должен возвращать DataFrame
    mock_read_excel.return_value = pd.DataFrame({
        'Name': ['Alice', 'Bob'],
        'Amount': [100, 200],
        'Currency': ['RUB', 'USD']
    })

    file_path = os.path.join(TEST_DATA_DIR, 'dummy.xlsx') #Абсолютный путь НЕ нужен для теста с mock_read_excel
    expected_result = [
        {'Name': 'Alice', 'Amount': 100, 'Currency': 'RUB'},
        {'Name': 'Bob', 'Amount': 200, 'Currency': 'USD'}
    ]

    result = read_transactions_from_excel(file_path)
    assert result == expected_result

@patch("os.path.exists", return_value=False)
def test_read_transactions_from_excel_file_not_found(mock_exists):
    result = read_transactions_from_excel('non_existent_file.xlsx')
    assert result == []

@patch('pandas.read_excel')
@patch("os.path.exists", return_value=True) # Добавлена эта строка
def test_read_transactions_from_excel_invalid_data(mock_exists,mock_read_excel):
    mock_read_excel.side_effect = ValueError("Ошибка чтения Excel файла")
    with pytest.raises(ValueError):
        read_transactions_from_excel(os.path.join(TEST_DATA_DIR, 'dummy.xlsx'))
