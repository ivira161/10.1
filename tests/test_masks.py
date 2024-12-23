import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234 5678 9123 4567", "1234 56** **** 4567"),  # валидный номер карты
        ("0000 0000 0000 0000", "0000 00** **** 0000"),  # другой валидный номер
        ("1234 5678 9123", pytest.raises(ValueError)),  # слишком короткий номер карты
        ("1234 5678 9123 456 7890", pytest.raises(ValueError)),  # слишком длинный номер карты
    ]
)
def test_get_mask_card_number(card_number, expected):
    if isinstance(expected, str):
        assert get_mask_card_number(card_number) == expected
    else:
        with expected:
            get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("123456789", "**6789"),  # валидный номер счета
        ("123", pytest.raises(ValueError)),  # слишком короткий номер счета
        ("12ab", pytest.raises(ValueError)),  # невалидные символы
    ]
)
def test_get_mask_account(account_number, expected):
    if isinstance(expected, str):
        assert get_mask_account(account_number) == expected
    else:
        with expected:
            get_mask_account(account_number)
