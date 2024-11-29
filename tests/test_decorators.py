import pytest
from src.decorators import log


@log()
def my_function(x, y):
    return x + y


def test_function():
    result = my_function(1, 2)
    assert result == 3  # Проверка, что 1 + 2 равно 3


@log()
def my_function_with_error(x, y):
    return x / y


def test_function_with_error(capsys):
    with pytest.raises(ZeroDivisionError):
        my_function_with_error(1, 0)  # Вызов с аргументами, приводящими к ошибке

    # Перехват выводов в консоль
    captured = capsys.readouterr()
    assert "'my_function_with_error' error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out
