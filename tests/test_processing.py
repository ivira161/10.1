import pytest

from src.processing import filter_by_state, sort_by_date


def test_sort_by_date_with_invalid_date_format():
    # Тест на некорректные форматы дат
    data = [
        {'date': '2023-10-01'},
        {'date': 'invalid_date'},
        {'date': '2022-10-01'},
    ]

    with pytest.raises(ValueError):
        sort_by_date(data)


def test_filter_by_state():
    # Тест на пустой список
    assert filter_by_state([]) == []
