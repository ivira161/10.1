import unittest
from unittest.mock import patch, mock_open
from src.utils import read_transactions_from_json, calculate_transaction_amount


class TestReadTransactionsFromJson(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='')
    @patch("os.path.exists", return_value=True)
    def test_empty_file(self, mock_exists, mock_file):
        result = read_transactions_from_json('data/empty_file.json')
        self.assertEqual(result, [])  # Ожидаем пустой список

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    @patch("os.path.exists", return_value=True)
    def test_json_not_a_list(self, mock_exists, mock_file):
        result = read_transactions_from_json('data/invalid_list.json')
        self.assertEqual(result, [])  # Ожидаем пустой список


class TestCalculateTransactionAmount(unittest.TestCase):

    def test_missing_amount(self):
        transaction = {'currency': 'USD'}
        result = calculate_transaction_amount(transaction)
        self.assertEqual(result, 0.0)  # Ожидаем 0.0

    def test_missing_currency(self):
        transaction = {'amount': 100.0}
        result = calculate_transaction_amount(transaction)
        self.assertEqual(result, 100.0)  # Ожидаем, что вернется сумма без изменений

    def test_negative_amount(self):
        transaction = {'amount': -100.0, 'currency': 'USD'}
        result = calculate_transaction_amount(transaction)
        self.assertEqual(result, -100.0)  # Ожидаем, что вернется отрицательная сумма

    @patch('src.external_api.convert_to_rub', return_value=75.0)
    def test_positive_amount_conversion(self, mock_convert):
        transaction = {'amount': 100.0, 'currency': 'USD'}
        result = calculate_transaction_amount(transaction)
        self.assertEqual(result, 75.0)  # Ожидаем, что вернется конвертированная сумма

    def test_unsupported_currency(self):
        transaction = {'amount': 100.0, 'currency': 'JPY'}
        result = calculate_transaction_amount(transaction)
        self.assertEqual(result, 100.0)  # Ожидаем, что вернется сумма без изменений

    def test_zero_amount(self):
        transaction = {'amount': 0.0, 'currency': 'USD'}
        result = calculate_transaction_amount(transaction)
        self.assertEqual(result, 0.0)  # Ожидаем, что вернется 0.0


if __name__ == '__main__':
    unittest.main()
