import unittest
from unittest.mock import mock_open, patch

import pandas as pd
from files.file_operations import read_transactions_from_csv, read_transactions_from_excel  # Замените на Ваш модуль


class TestFileOperations(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='Name,Amount,Currency\nAlice,100,RUB\nBob,200,USD')
    def test_read_transactions_from_csv(self, mock_file):
        file_path = 'dummy.csv'
        expected_result = [
            {'Name': 'Alice', 'Amount': '100', 'Currency': 'RUB'},
            {'Name': 'Bob', 'Amount': '200', 'Currency': 'USD'}
        ]
        result = read_transactions_from_csv(file_path)
        self.assertEqual(result, expected_result)

    @patch('pandas.read_excel')
    def test_read_transactions_from_excel(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame({
            'Name': ['Alice', 'Bob'],
            'Amount': [100, 200],
            'Currency': ['RUB', 'USD']
        })
        file_path = 'dummy.xlsx'
        expected_result = [
            {'Name': 'Alice', 'Amount': 100, 'Currency': 'RUB'},
            {'Name': 'Bob', 'Amount': 200, 'Currency': 'USD'}
        ]
        result = read_transactions_from_excel(file_path)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
