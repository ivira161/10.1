import sys
from typing import List, Dict, Any
from src.utils import read_json_transactions, read_csv_transactions, read_excel_transactions, search_transactions


def ask_yes_no(question: str) -> bool:
    """
    Универсальная функция для уточнения у пользователя,
    нужен ли определённый шаг (да/нет).
    Если пользователь вводит что-то другое, мы просим повторить ввод.
    :return: True, если пользователь ответил "да", False, если "нет".
    """
    while True:
        user_input = input(question).strip().lower()
        if user_input == "да":
            return True
        elif user_input == "нет":
            return False
        else:
            print('Некорректный ввод. Пожалуйста, введите "Да" или "Нет".')


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ").strip()
    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        file_path = "operations.json"
        transactions = read_json_transactions(file_path)
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        file_path = "transactions.csv"
        transactions = read_csv_transactions(file_path)
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        file_path = "transactions_excel.xlsx"
        transactions = read_excel_transactions(file_path)
    else:
        print("Неправильный выбор. Программа завершается.")
        sys.exit(0)

    if not transactions:
        print("Не удалось получить транзакции из выбранного файла либо файл пуст.")
        sys.exit(0)

    # print(f"Всего транзакций: {len(transactions)}")
    # # Пример: выводим первые 5
    # for i, txn in enumerate(transactions[:5], start=1):
    #     print(f"{i}. {txn}")

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")
        user_status = input("Пользователь: ").strip().upper()
        if user_status not in valid_statuses:
            print(f'Программа: Статус операции "{user_status}" недоступен.')
        else:
            print(f'Программа: Операции отфильтрованы по статусу "{user_status}"')
            break

    filtered_transactions = [
        t for t in transactions if t.get("state", "").upper() == user_status
    ]

    # Спросим, нужно ли сортировать операции по дате
    if ask_yes_no("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: "):
        # Спросим, по возрастанию или убыванию
        while True:
            sort_direction = input(
                "Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
            if sort_direction not in ["по возрастанию", "по убыванию"]:
                print('Пожалуйста, введите "по возрастанию" или "по убыванию".')
            else:
                reverse_sort = (sort_direction == "по убыванию")
                # Сортируем по дате
                from datetime import datetime

                def parse_date(dt_str):
                    try:
                        # Удаляем возможный символ 'Z'
                        return datetime.fromisoformat(dt_str.replace("Z", ""))
                    except ValueError:
                        return datetime.min

                filtered_transactions.sort(key=lambda x: parse_date(x.get("date", "")), reverse=reverse_sort)
                break

    # Спросим, нужно ли выводить только рублёвые операции
    if ask_yes_no("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: "):
        def is_rub(txn):
            # Для CSV/Excel (поле currency_code), для JSON (operationAmount->currency->code)
            code_csv = txn.get("currency_code", "").upper()
            code_json = txn.get("operationAmount", {}).get("currency", {}).get("code", "").upper()
            return code_csv == "RUB" or code_json == "RUB"

        filtered_transactions = [t for t in filtered_transactions if is_rub(t)]

    # Спросим, нужно ли отфильтровать по определённому слову в описании
    if ask_yes_no(
            "Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: "):
        search_str = input("Программа: Введите строку для поиска:\nПользователь: ")
        filtered_transactions = search_transactions(filtered_transactions, search_str)

    # Финальный вывод
    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    count_tx = len(filtered_transactions)
    if count_tx == 0:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print(f"Программа:\nВсего банковских операций в выборке: {count_tx}\n")
        for txn in filtered_transactions:
            print(f"Дата операции: {txn.get('date')}")
            print(f"Описание: {txn.get('description')}")
            print(f"Сумма: {txn.get('amount') or txn.get('operationAmount', {}).get('amount', 'N/A')} "
                  f"{txn.get('currency_code') or txn.get('operationAmount', {}).get('currency', {}).get('code', 'N/A')}")
            print(f"Статус: {txn.get('state')}")
            print("-" * 50)


if __name__ == "__main__":
    main()
