from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: str) -> str:
    """Функция, которая умеет обрабатывать информацию как о картах, так и о счетах"""

    parts = input_string.split()  # Разделяем строку на слова по пробелам

    if len(parts) < 2:
        return "Неверный формат ввода"  # Обработка некорректного ввода

    card_type = " ".join(parts[:-1])  # Объединяем все слова, кроме последнего
    card_number = parts[-1]  # Последнее слово - номер карты/счета

    if card_type.startswith("Visa") or card_type.startswith("Maestro") or card_type.startswith("MasterCard"):
        try:
            masked_number = get_mask_card_number(card_number)
            return f"{card_type} {masked_number}"
        except ValueError as e:
            return f"Ошибка: {e}"

    elif card_type.startswith("Счет"):
        try:
            masked_account = get_mask_account(card_number)
            return f"{card_type} {masked_account}"
        except ValueError as e:
            return f"Ошибка: {e}"

    else:
        return "Неизвестный тип карты/счета"


def get_date(input_list: str) -> str:
    """Функция, которая принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407" и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ" ("11.03.2024"). Если дата неполная, возвращает ошибку."""

    # Проверяем, что длина строки достаточна для извлечения даты
    if len(input_list) < 10:
        raise ValueError("Ошибка: Неполный формат даты.")

    new_input_list = input_list[:10].split("-")
    new_input_reversed = new_input_list[::-1]
    new_input_result = ".".join(new_input_reversed)
    return new_input_result
