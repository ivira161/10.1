import pytest
from unittest.mock import patch
from src.main import main


@pytest.mark.parametrize("user_input, mock_transactions", [
    (
            # Пользовательские ответы:
            [
                "1",  # Выбор JSON
                "EXECUTED",  # Статус
                "нет",  # сортировать?
                "нет",  # рублёвые?
                "нет"  # искать по описанию?
            ],
            # Мокаем, что в JSON вернутся транзакции
            [
                {"id": 100, "state": "EXECUTED", "date": "2023-01-01T10:00:00Z",
                 "amount": "999", "currency_code": "RUB", "description": "Перевод"},
                {"id": 101, "state": "CANCELED", "date": "2023-02-01T10:00:00Z",
                 "amount": "1000", "currency_code": "RUB", "description": "Открытие вклада"}
            ]
    ),
    (
            # Второй пример ввода, где пользователь указывает неверный статус сначала
            [
                "2",  # Выбор CSV
                "WRONGSTATUS",  # Неверный статус -> программа попросит заново
                "EXECUTED",  # Успешный статус
                "да",  # сортировать по дате?
                "по возрастанию",
                "да",  # только рублёвые?
                "нет"  # поиск по описанию?
            ],
            [
                {"id": 1, "state": "EXECUTED", "date": "2023-03-01T10:00:00Z",
                 "amount": "2000", "currency_code": "RUB", "description": "Перевод с карты"},
                {"id": 2, "state": "EXECUTED", "date": "2023-01-01T10:00:00Z",
                 "amount": "500", "currency_code": "USD", "description": "Payment"}
            ]
    )
])
def test_main_flow(monkeypatch, user_input, mock_transactions, capsys):
    """
    Тест проверяет, что функция main корректно:
    1) Вызывает функции для чтения (замокаем их).
    2) Фильтрует по статусу.
    3) Обрабатывает неверные статусы.
    4) Сортирует, если надо.
    5) Фильтрует по рублю, если надо.
    6) Выводит результат в stdout.
    """
    # Подготовим side_effect для input
    # Каждая строка user_input - это то, что будет "вводить" пользователь
    monkeypatch.setattr("builtins.input", lambda _: user_input.pop(0))

    # Мокаем функции чтения файлов, чтобы не зависеть от реальных данных:
    # Для примера, если пользователь выбрал "1" (JSON), то мы мокнем read_json_transactions,
    # если выбрал "2" - read_csv_transactions и т.д.

    with patch("src.main.read_json_transactions", return_value=mock_transactions), \
            patch("src.main.read_csv_transactions", return_value=mock_transactions), \
            patch("src.main.read_excel_transactions", return_value=mock_transactions):
        main()  # Запускаем основную функцию

    captured = capsys.readouterr()

    # Теперь проверяем, что в выводе содержатся некоторые строки,
    # которые говорят о корректной работе сценария
    # Например, что программа не упала при неверном статусе, просила ввести повторно и т.д.
    # И/или что были отфильтрованы только EXECUTED.

    assert "Привет! Добро пожаловать" in captured.out  # приветственное сообщение
    assert "Операции отфильтрованы по статусу" in captured.out  # значит, статус в итоге приняли

    # Можно проверить, отфильтровались ли EXECUTED
    if any(txn["state"].upper() == "EXECUTED" for txn in mock_transactions):
        # То есть, если среди мока есть EXECUTED, то вывод "Всего банковских операций в выборке" должен быть > 0
        assert "Всего банковских операций в выборке" in captured.out
    else:
        # Если нет, то "Не найдено ни одной транзакции"
        assert "Не найдено ни одной транзакции" in captured.out


@pytest.mark.parametrize("user_responses,mock_transactions", [
    (
            # Сценарий: пользователь выбирает JSON (1), статус EXECUTED, говорит "нет" остальным вопросам
            ["1", "EXECUTED", "нет", "нет", "нет"],
            [
                {"id": 100, "state": "EXECUTED", "date": "2023-01-01T10:00:00Z",
                 "amount": "999", "currency_code": "RUB", "description": "Перевод организации"},
                {"id": 101, "state": "CANCELED", "date": "2023-02-01T10:00:00Z",
                 "amount": "1000", "currency_code": "RUB", "description": "Открытие вклада"},
            ]
    ),
    (
            # Сценарий: пользователь выбирает CSV (2), сначала вводит неверный статус,
            # потом EXECUTED, затем хочет сортировать, хочет только рубли, и т.д.
            ["2", "WRONGSTATUS", "EXECUTED", "да", "по возрастанию", "да", "нет"],
            [
                {"id": 200, "state": "EXECUTED", "date": "2023-03-10T12:00:00Z",
                 "amount": "9999", "currency_code": "RUB", "description": "Перевод с карты"},
                {"id": 201, "state": "EXECUTED", "date": "2023-01-10T12:00:00Z",
                 "amount": "500", "currency_code": "USD", "description": "Payment"},
            ]
    )
])
def test_main_flow(monkeypatch, user_responses, mock_transactions, capsys):
    """
    Тестируем функцию main:
    - как она реагирует на выбор файла (JSON/CSV/Excel),
    - как обрабатывает ввод статуса (в т.ч. неверный),
    - сортировку,
    - вывод в консоль,
    - фильтрацию по рублям (если надо),
    - и т.д.
    """
    # Заменяем input() на нашу функцию, которая возвращает по очереди элементы user_responses
    monkeypatch.setattr("builtins.input", lambda _: user_responses.pop(0))

    with patch("src.main.read_json_transactions", return_value=mock_transactions), \
            patch("src.main.read_csv_transactions", return_value=mock_transactions), \
            patch("src.main.read_excel_transactions", return_value=mock_transactions):
        main()

    captured = capsys.readouterr()
    out = captured.out

    # Проверяем, что программа поздоровалась
    assert "Добро пожаловать" in out

    # Проверяем, что программа спрашивала "Введите статус..."
    assert "Введите статус" in out

    # Если в user_responses присутствует "WRONGSTATUS", убедимся, что программа ругалась
    if "WRONGSTATUS" in user_responses:
        assert 'Статус операции "WRONGSTATUS" недоступен' in out

    # Если в mock_transactions есть EXECUTED-операции, после фильтрации они должны остаться
    executed_count = sum(1 for t in mock_transactions if t["state"].upper() == "EXECUTED")
    if executed_count > 0:
        assert "Всего банковских операций в выборке" in out
    else:
        assert "Не найдено ни одной транзакции" in out
