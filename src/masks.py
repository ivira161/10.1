def get_mask_card_number(card_number: str) -> str:
    # Убираем пробелы из номера карты
    card_number = card_number.replace(" ", "")
    # Проверяем длину номера карты
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр.")

    # Маскируем номер карты
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    return masked_number


def get_mask_account(account_number: str) -> str:
    # Проверяем номер на наличие только цифр и минимальную длину
    if not account_number.isdigit() or len(account_number) < 4:
        raise ValueError("Номер счета должен содержать только цифры и иметь минимум 4 цифры.")

    # Маскируем номер счета
    masked_account_number = f"**{account_number[-4:]}"

    return masked_account_number
