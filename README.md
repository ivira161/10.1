## Описание

Виджет банковских операций клиента.

## Установка

1. Клонирование репозитория
   [GitHub](git@github.com:ivira161/10.1.git)
2. Установка зависимостей
   `poetry install`

## Тестирование
Все функции проекта протестированы с оценкой покрытия - 87%

## Модуль `generation`'

Модуль `generation` предоставляет функции для управления транзакциями и работы с номерами банковских карт. Все функции написаны с использованием генераторов для эффективной обработки данных.

## Функции

### 1. `filter_by_currency(transactions, target_currency)`

Функция принимает на вход список словарей, представляющих транзакции, и возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной (например, "USD").

**Параметры:**
- `transactions` (List[Dict[str, Any]]): Список транзакций.
- `target_currency` (str): Целевая валюта для фильтрации (например, "USD").

**Пример использования:**

```python
transactions = [
    {
        "id": 1,
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    },
    {
        "id": 2,
        "operationAmount": {
            "amount": "200.00",
            "currency": {
                "code": "EUR"
            }
        }
    }
]

filtered = filter_by_currency(transactions, "USD")
for transaction in filtered:
    print(transaction)
```
### 2. transaction_descriptions(transactions)

Генератор, который принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.

Параметры:

    transactions (List[Dict[str, Any]]): Список транзакций.

Пример использования:

```Python

transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"description": None}
]

descriptions = transaction_descriptions(transactions)
for desc in descriptions:
    print(desc)  # Выведет: "Перевод организации", "Перевод со счета на счет", "Нет описания"
```
### 3. card_number_generator(start, end)

Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты. Генератор может сгенерировать номера карт в заданном диапазоне.
Он может быть использован, например, для генерации тестовых данных или в приложениях, где необходимы временные номера карт.
Параметры:

    start (int): Начальное значение диапазона.
    end (int): Конечное значение диапазона.

Пример использования:

```Python

for card_number in card_number_generator(1, 3):
    print(card_number)  
# Выведет:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
```
