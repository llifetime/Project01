import json
import os
from urllib.error import URLError
from urllib.request import urlopen

from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env


def convert_currency(amount: float, currency: str) -> float:
    """
    Конвертирует сумму через API ЦБ РФ или сторонний сервис.
    """
    if currency not in ('USD', 'EUR'):
        raise ValueError(f"Unsupported currency: {currency}")

    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if api_key:
        # Используем платный API с ключом (пример)
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{currency}/RUB/{amount}"
        try:
            with urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                return float(data['conversion_result'])
        except (URLError, KeyError, json.JSONDecodeError) as e:
            raise ValueError(f"API request failed: {str(e)}")
    else:
        # Fallback: API ЦБ РФ (бесплатно)
        try:
            with urlopen('https://www.cbr-xml-daily.ru/daily_json.js') as response:
                data = json.loads(response.read().decode('utf-8'))
                rate = data['Valute'][currency]['Value']
                return amount * rate
        except (URLError, KeyError) as e:
            raise ValueError(f"CBR API failed: {str(e)}")
