import pytest
from datetime import datetime
from src.processing import sort_by_date, filter_by_state

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


