import pytest

from src.generation import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency(transactions):
    target_currency = "USD"
    filtered_transactions = list(filter_by_currency(transactions, target_currency))

    assert len(filtered_transactions) == 3  # Проверяем, что 3 транзакции соответствуют USD
    assert all(tx['operationAmount']['currency']['code'] == target_currency for tx in
               filtered_transactions)  # Проверяем, что все транзакции имеют валюту USD
    assert filtered_transactions, "Список пустой!"  # Проверяем, пустой список или нет

    # Тестируем генератор описания


def test_transaction_descriptions(transactions):
    descriptions = list(transaction_descriptions(transactions))

    # Проверяем, что мы получили ожидаемые описания
    assert descriptions == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод со счета на счет"
    ]

    # Проверяем, что длина списка описаний соответствует количеству транзакций
    assert len(descriptions) == len(transactions)

    # Проверяем, что генератор возвращает значение по умолчанию для отсутствующих описаний
    empty_transactions = [{}]  # Транзакция без описания
    empty_descriptions = list(transaction_descriptions(empty_transactions))
    assert empty_descriptions == ["Нет описания"]


@pytest.mark.parametrize("start, end, expected", [
    (1, 1, ["0000 0000 0000 0001"]),
    (1, 5, ["0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005"]),
    (10, 12, ["0000 0000 0000 0010",
              "0000 0000 0000 0011",
              "0000 0000 0000 0012"]),
    (100, 100, ["0000 0000 0000 0100"])
])
def test_card_number_generator(start, end, expected):
    assert list(card_number_generator(start, end)) == expected


# Тест для пустого диапазона:
@pytest.mark.parametrize("start, end, expected", [
    (1, 0, []),  # Пустой диапазон
])
def test_card_number_generator_empty_range(start, end, expected):
    with pytest.raises(ValueError, match="Начальный диапазон не может быть больше конечного"):
        list(card_number_generator(start, end))


# Тест для диапазона с одним значением:
@pytest.mark.parametrize("start, end, expected", [
    (5, 5, ["0000 0000 0000 0005"]),  # Проверка для одного значения
])
def test_card_number_generator_single_value(start, end, expected):
    assert list(card_number_generator(start, end)) == expected


# Тест для диапазона, включающего максимальный номер карты:
@pytest.mark.parametrize("start, end, expected", [
    (9998, 10000, [
        "0000 0000 0000 9998",
        "0000 0000 0000 9999",
        "0000 0000 0001 0000"
    ]),  # Проверка на большом диапазоне
])
def test_card_number_generator_large_range(start, end, expected):
    assert list(card_number_generator(start, end)) == expected
