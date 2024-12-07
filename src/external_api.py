import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://apilayer.com/exchangerates_data-api"
API_KEY = os.getenv("EXCHANGE_API_KEY")  # Токен доступа из .env


def convert_to_rub(amount: float, currency: str) -> float:
    """
    Конвертирует сумму в указанной валюте в рубли.


    :param amount: Сумма для конвертации.
    :param currency: Валюта, в которой указана сумма.
    :return: Сумма в рублях.
    """
    if currency not in ['USD', 'EUR']:
        return amount  # Если валюта не USD или EUR, возвращаем сумму без изменений

    response = requests.get(f"{API_URL}/convert?to=RUB&from={currency}&amount={amount}",
                            headers={"apikey": API_KEY})

    if response.status_code == 200:
        data = response.json()
        return data['result']
    else:
        print("Ошибка при получении данных с API.")
        return amount  # Возвращаем исходную сумму в случае ошибки
