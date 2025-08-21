import pytest
from src.utils import get_transaction_amount_in_rub, exchange_service


class TestTransactionConversion:

    def test_usd_conversion_real_api(self):
        """Тест конвертации USD в RUB с реальным API"""
        transaction = {
            'amount': '100.00',
            'currency': 'USD',
            'description': 'Test transaction'
        }

        result = get_transaction_amount_in_rub(transaction)

        # Проверяем что результат является числом и положительным
        assert isinstance(result, float)
        assert result > 0
        print(f"USD to RUB conversion result: {result}")

    def test_eur_conversion_real_api(self):
        """Тест конвертации EUR в RUB с реальным API"""
        transaction = {
            'amount': '50.00',
            'currency': 'EUR',
            'description': 'Test transaction'
        }

        result = get_transaction_amount_in_rub(transaction)

        assert isinstance(result, float)
        assert result > 0
        print(f"EUR to RUB conversion result: {result}")

    def test_rub_no_conversion(self):
        """Тест что RUB не конвертируется"""
        transaction = {
            'amount': '1000.00',
            'currency': 'RUB',
            'description': 'Test transaction'
        }

        result = get_transaction_amount_in_rub(transaction)
        assert result == 1000.0

    def test_exchange_service_direct(self):
        """Прямой тест сервиса курсов"""
        rate = exchange_service.get_exchange_rate('USD')
        assert rate is not None
        assert isinstance(rate, float)
        assert rate > 0
        print(f"Current USD rate: {rate}")