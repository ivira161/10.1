import unittest
from unittest.mock import Mock, patch

from src.external_api import calculate_and_convert_transaction_amount


class TestCalculateAndConvertTransactionAmount(unittest.TestCase):

    @patch('src.external_api.requests.get')
    def test_valid_conversion(self, mock_get):
        # Настраиваем мок для успешного запроса
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 75.0}  # Примерный результат конвертации
        mock_get.return_value = mock_response

        transaction = {'amount': 100.0, 'currency': 'USD'}
        result = calculate_and_convert_transaction_amount(transaction)
        self.assertEqual(result, 75.0)  # Ожидаем, что вернется конвертированная сумма

    @patch('src.external_api.requests.get')
    def test_invalid_currency(self, mock_get):
        transaction = {'amount': 100.0, 'currency': 'JPY'}
        result = calculate_and_convert_transaction_amount(transaction)
        self.assertEqual(result, 100.0)  # Ожидаем, что вернется сумма без изменений

    @patch('src.external_api.requests.get')
    def test_api_error(self, mock_get):
        # Настраиваем мок для ошибки API
        mock_response = Mock()
        mock_response.status_code = 400  # Ошибка от API
        mock_get.return_value = mock_response

        transaction = {'amount': 100.0, 'currency': 'USD'}
        result = calculate_and_convert_transaction_amount(transaction)
        self.assertEqual(result, 100.0)  # Ожидаем, что вернется исходная сумма

    def test_negative_amount(self):
        transaction = {'amount': -100.0, 'currency': 'USD'}
        result = calculate_and_convert_transaction_amount(transaction)
        self.assertEqual(result, -100.0)  # Ожидаем, что вернется отрицательная сумма

    def test_zero_amount(self):
        transaction = {'amount': 0.0, 'currency': 'USD'}
        result = calculate_and_convert_transaction_amount(transaction)
        self.assertEqual(result, 0.0)  # Ожидаем, что вернется 0.0


if __name__ == '__main__':
    unittest.main()
