import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data"
API_KEY = os.getenv("EXCHANGE_API_KEY")  # Токен доступа из .env


def calculate_and_convert_transaction_amount(transaction: dict) -> float:
    """
    Рассчитывает сумму транзакции в рублях.

    :param transaction: Словарь с данными о транзакции.
    :return: Сумма транзакции в рублях.
    """
    amount = transaction.get('amount', 0.0)
    currency = transaction.get('currency', 'RUB')

    if amount < 0:
        return amount  # Возвращаем отрицательную сумму без конвертации

    if currency not in ['USD', 'EUR']:
        return float(amount)  # Если валюта не USD или EUR, возвращаем сумму без изменений

    print(f"Запрос к API: {API_URL}/convert?to=RUB&from={currency}&amount={amount}")  # Для отладки
    print(f"Используемый API ключ: {API_KEY}")  # Для отладки

    response = requests.get(f"{API_URL}/convert?to=RUB&from={currency}&amount={amount}",
                            headers={"apikey": API_KEY})

    if response.status_code == 200:
        data = response.json()
        return float(data['result'])  # Преобразуем результат в float перед возвратом
    else:
        print(f"Ошибка при получении данных с API. Статус код: {response.status_code}, Ответ: {response.text}")
        return float(amount)  # Возвращаем исходную сумму в случае ошибки


# Пример вызова функции
transaction = {'amount': 20.00, 'currency': 'USD'}
result = calculate_and_convert_transaction_amount(transaction)
print(f"Конвертированная сумма: {result}")
