def filter_by_currency(transactions, target_currency):
    '''Функция, которая принимает на вход список словарей, представляющих транзакции,
    и возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD)'''

    for transaction in transactions:
        if transaction['operationAmount']['currency']['code'] == target_currency:
            yield transaction


def transaction_descriptions(transactions):
    '''Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди'''

    for transaction in transactions:
        yield transaction.get('description', 'Нет описания')


def card_number_generator(start, end):
    '''Генератор, который выдает номера банковских карт в формате
       XXXX XXXX XXXX XXXX, где X — цифра номера карты.
       Генератор может сгенерировать номера карт в заданном диапазоне
       от 0000 0000 0000 0001 до 9999 9999 9999 9999.
       Генератор должен принимать начальное и конечное значения
       для генерации диапазона номеров.'''
    if start > end:  # Проверка на корректность диапазона
        raise ValueError("Начальный диапазон не может быть больше конечного")
    # Основной цикл генератора
    for number in range(start, end + 1):
        card_number = f"{number:0>16}"  # Форматируем номер карты, добавляя нули спереди
        formatted_card_number = ' '.join(card_number[i:i + 4] for i in range(0, len(card_number), 4))  # Разбиваем на группы по 4
        yield formatted_card_number  # Генерируем отформатированный номер карты


