import json
import pytest
from unittest.mock import mock_open, patch
from src.utils import (
    read_csv_transactions,
    read_json_transactions,
    read_excel_transactions,
    search_transactions,
    count_categories
)


@pytest.fixture
def mock_csv_data():
    return """id;state;date;amount;currency_name;currency_code;from;to;description
1;EXECUTED;2023-01-01T10:00:00Z;100;Rub;RUB;Visa 1234;Счет 5678;Перевод с карты на карту
2;CANCELED;2023-01-02T10:00:00Z;200;Rub;RUB;Mastercard 9999;Счет 8888;Открытие вклада
"""


def test_read_csv_transactions(mock_csv_data):
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        result = read_csv_transactions("fake_path.csv")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["description"] == "Открытие вклада"


def test_read_json_transactions():
    mock_json_data = json.dumps([
        {"id": 123, "state": "EXECUTED", "description": "Test JSON"}
    ])
    with patch("builtins.open", mock_open(read_data=mock_json_data)) as _:
        result = read_json_transactions("fake_path.json")
    assert len(result) == 1
    assert result[0]["id"] == 123

    # Тест на пустой JSON
    with patch("builtins.open", mock_open(read_data="")) as _:
        result_empty = read_json_transactions("fake_path.json")
    assert result_empty == []


@pytest.mark.skipif("openpyxl" not in globals(), reason="openpyxl not installed")
def test_read_excel_transactions():
    # Этот тест условно мокаем openpyxl
    with patch("openpyxl.load_workbook") as mock_wb:
        mock_ws = [
            # Первая строка - заголовки
            [MockCell("id"), MockCell("state"), MockCell("date"), MockCell("description")],
            # Данные
            [MockCell(1), MockCell("EXECUTED"), MockCell("2023-01-01"), MockCell("Test transaction")],
        ]
        mock_sheet = MockSheet(mock_ws)
        instance_wb = mock_wb.return_value
        instance_wb.active = mock_sheet

        result = read_excel_transactions("fake_path.xlsx")
        assert len(result) == 1
        assert result[0]["description"] == "Test transaction"


def test_search_transactions():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "перевод с карты на карту"}
    ]
    found = search_transactions(transactions, "Перевод")
    assert len(found) == 2
    found_case = search_transactions(transactions, "перЕВОд")
    assert len(found_case) == 2


def test_count_categories():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "перевод с карты на карту"},
        {"description": "ПЕРЕВОД СО СЧЁТА НА СЧЁТ"}
    ]
    categories = ["Перевод", "Открытие вклада", "test_cat"]
    result = count_categories(transactions, categories)
    assert result["Перевод"] == 3
    assert result["Открытие вклада"] == 1
    # "test_cat" либо нет в словаре, либо 0
    assert "test_cat" not in result or result["test_cat"] == 0


# Вспомогательные классы для мока Excel
class MockCell:
    def __init__(self, value):
        self.value = value


class MockSheet:
    def __init__(self, rows):
        self._rows = rows

    @property
    def rows(self):
        for row in self._rows:
            yield row


@pytest.fixture
def csv_data():
    return """id;state;date;amount;currency_name;currency_code;from;to;description
1;EXECUTED;2023-01-01T10:00:00Z;100;Ruble;RUB;Visa 1234;Счет 5678;Перевод с карты на карту
2;CANCELED;2023-01-02T10:00:00Z;200;Dollar;USD;Mastercard 9999;Счет 8888;Открытие вклада
"""


@pytest.fixture
def json_data():
    return json.dumps([
        {"id": 101, "state": "EXECUTED", "description": "Test JSON"},
        {"id": 202, "state": "PENDING", "description": "Another JSON"},
    ])


def test_read_csv_transactions(csv_data):
    with patch("builtins.open", mock_open(read_data=csv_data)):
        result = read_csv_transactions("fake.csv")

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["description"] == "Перевод с карты на карту"
    assert result[1]["state"] == "CANCELED"


def test_read_json_transactions(json_data):
    # Проверяем чтение нормального JSON
    with patch("builtins.open", mock_open(read_data=json_data)):
        result = read_json_transactions("fake.json")
    assert len(result) == 2
    assert result[0]["id"] == 101

    # Проверяем случай, когда файл пустой
    with patch("builtins.open", mock_open(read_data="")):
        result_empty = read_json_transactions("fake_empty.json")
    assert result_empty == []


def test_read_excel_transactions():
    # Здесь нужно замокать openpyxl.load_workbook
    # Если у вас внутри read_excel_transactions используется openpyxl
    # или pandas.read_excel, мокайте соответствующие вызовы.
    with patch("src.utils.openpyxl.load_workbook") as mock_wb:
        # Мокаем возвращаемый workbook + sheet
        mock_ws = [
            # первая строка — заголовки
            [MockCell("id"), MockCell("state"), MockCell("date"), MockCell("description")],
            # строка данных
            [MockCell(999), MockCell("EXECUTED"), MockCell("2023-01-01T10:00:00Z"), MockCell("Test Excel")],
        ]
        mock_sheet = MockSheet(mock_ws)
        instance_wb = mock_wb.return_value
        instance_wb.active = mock_sheet

        result = read_excel_transactions("fake.xlsx")
        assert len(result) == 1
        assert result[0]["id"] == 999
        assert result[0]["description"] == "Test Excel"


def test_search_transactions():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "перевод с карты на карту"},
    ]
    found = search_transactions(transactions, "Перевод")
    assert len(found) == 2  # два совпадения ("Перевод организации", "перевод с карты")
    # ignore case
    found_case = search_transactions(transactions, "пЕреВоД")
    assert len(found_case) == 2


def test_count_categories():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "перевод с карты на карту"},
        {"description": "ПЕРЕВОД СО СЧЁТА НА СЧЁТ"},
    ]
    categories = ["Перевод", "Открытие вклада"]
    counts = count_categories(transactions, categories)
    # "Перевод" встречается 3 раза (регистронезависимо, если у вас так сделано)
    assert counts["Перевод"] == 3
    assert counts["Открытие вклада"] == 1


# Вспомогательные классы для мока Excel
class MockCell:
    def __init__(self, value):
        self.value = value


class MockSheet:
    def __init__(self, rows):
        self._rows = rows

    @property
    def rows(self):
        for row in self._rows:
            yield row
