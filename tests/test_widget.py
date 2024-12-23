import pytest
from src.widget import mask_account_card, get_date

@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),  # Изменено на 16 цифр без пробелов
        ("Счет 123456789", "Счет **6789"),
        ("Ошибка", "Неверный формат ввода"),
        ("Счет", "Неверный формат ввода"),
        ("Visa 1234", "Ошибка: Номер карты должен содержать 16 цифр."),
    ]
)
def test_mask_account_card(input_string, expected):
    assert mask_account_card(input_string) == expected

@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03", "03.2024"),  # Проверка не полного формата
    ]
)
def test_get_date(input_date, expected):
    assert get_date(input_date) == expected