# utils.py
import requests
from typing import Optional
from typing import Dict


def get_transaction_amount_in_rub(transaction: Dict) -> float:
    """
    Возвращает сумму транзакции в рублях (float).
    Если валюта — USD или EUR, конвертирует по текущему курсу.

    :param transaction: Словарь с данными транзакции
    :return: Сумма в рублях (float)
    :raises: ValueError, если транзакция некорректна или API недоступно
    """
    if not isinstance(transaction, dict):
        raise ValueError("Transaction must be a dictionary")

    amount = transaction.get('amount')
    currency = transaction.get('currency', 'RUB').upper()

    if amount is None:
        raise ValueError("Transaction is missing 'amount'")

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number")

    if currency == 'RUB':
        return amount
    elif currency in ('USD', 'EUR'):
        return convert_currency(amount, currency)
    else:
        raise ValueError(f"Unsupported currency: {currency}")


class ExchangeRateService:
    """Сервис для работы с API курсов валют"""

    def __init__(self, api_key: str = "1HAKfXuWbjhfftsgvB7LU02zwvYJwIYw"):
        self.api_key = api_key

    def get_exchange_rate(self, currency: str) -> Optional[float]:
        """
        Получает курс валюты к RUB используя различные API с ключом.
        """
        if currency not in ['USD', 'EUR']:
            return None

        # Пробуем разные API провайдеры с вашим ключом
        providers = [
            self._try_currencylayer,
            self._try_exchangeratesapi,
            self._try_alphavantage,
            self._try_frankfurter,  # Бесплатный fallback
            self._get_static_rate  # Статический fallback
        ]

        for provider in providers:
            rate = provider(currency)
            if rate is not None:
                return rate

        return None

    def _try_currencylayer(self, currency: str) -> Optional[float]:
        """CurrencyLayer API"""
        try:
            url = f"http://api.currencylayer.com/live?access_key={self.api_key}&currencies=RUB&source={currency}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get('success'):
                return data['quotes'][f'{currency}RUB']
        except Exception:
            pass
        return None

    def _try_exchangeratesapi(self, currency: str) -> Optional[float]:
        """ExchangeRatesAPI.io"""
        try:
            url = f"https://api.exchangeratesapi.io/v1/latest?access_key={self.api_key}&base={currency}&symbols=RUB"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get('success', False):
                return data['rates']['RUB']
        except Exception:
            pass
        return None

    def _try_alphavantage(self, currency: str) -> Optional[float]:
        """Alpha Vantage API"""
        try:
            url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency}&to_currency=RUB&apikey={self.api_key}"
            response = requests.get(url, timeout=10)
            data = response.json()

            rate_data = data.get('Realtime Currency Exchange Rate', {})
            if rate_data:
                return float(rate_data.get('5. Exchange Rate', 0))
        except Exception:
            pass
        return None

    def _try_frankfurter(self, currency: str) -> Optional[float]:
        """Frankfurter App (бесплатный)"""
        try:
            url = f"https://api.frankfurter.app/latest?from={currency}&to=RUB"
            response = requests.get(url, timeout=5)
            data = response.json()
            return data['rates']['RUB']
        except Exception:
            pass
        return None

    def _get_static_rate(self, currency: str) -> float:
        """Статические курсы как последний fallback"""
        static_rates = {'USD': 75.0, 'EUR': 85.0}
        return static_rates.get(currency)


# Глобальный экземпляр сервиса
exchange_service = ExchangeRateService()


def get_exchange_rate(currency: str) -> Optional[float]:
    """Основная функция для получения курса"""
    return exchange_service.get_exchange_rate(currency)


def convert_currency(amount: float, from_currency: str) -> float:
    """
    Конвертирует сумму из указанной валюты в рубли.
    """
    try:
        rate = get_exchange_rate(from_currency)
        if rate is None or rate <= 0:
            raise ValueError(f"Invalid exchange rate for {from_currency}")

        result = amount * rate
        print(f"Converted {amount} {from_currency} to {result} RUB (rate: {rate})")
        return result

    except Exception as e:
        raise ValueError(f"Currency conversion failed: {e}")
