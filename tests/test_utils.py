import unittest
from unittest.mock import patch, mock_open
from src.utils import read_transactions_from_json


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


if __name__ == '__main__':
    unittest.main()
