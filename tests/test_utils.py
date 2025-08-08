import unittest
from unittest.mock import patch, MagicMock
from src.utils import get_transaction_amount_in_rub
from src.external_api import convert_currency


class TestTransactionConversion(unittest.TestCase):
    @patch('external_api.convert_currency')
    def test_usd_conversion(self, mock_convert):
        mock_convert.return_value = 7500.0
        transaction = {"amount": 100, "currency": "USD"}
        result = get_transaction_amount_in_rub(transaction)
        self.assertEqual(result, 7500.0)
        mock_convert.assert_called_once_with(100.0, 'USD')

    def test_rub_no_conversion(self):
        transaction = {"amount": 5000, "currency": "RUB"}
        result = get_transaction_amount_in_rub(transaction)
        self.assertEqual(result, 5000.0)

    @patch('urllib.request.urlopen')
    def test_cbr_api_fallback(self, mock_urlopen):
        # Эмулируем ответ API ЦБ РФ
        mock_response = MagicMock()
        mock_response.read.return_value = b'''
        {
            "Valute": {
                "USD": {"Value": 75.5},
                "EUR": {"Value": 85.3}
            }
        }
        '''
        mock_urlopen.return_value = mock_response

        # Тест для USD
        result = convert_currency(100, 'USD')
        self.assertEqual(result, 7550.0)

        # Тест для EUR
        result = convert_currency(50, 'EUR')
        self.assertEqual(result, 4265.0)


if __name__ == '__main__':
    unittest.main()
