import logging

# Настройка логирования
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logs/masks.log')
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

# Примеры логирования
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')


def get_mask_card_number(card_number: str) -> str:
    # Убираем пробелы из номера карты
    card_number = card_number.replace(" ", "")

    # Проверяем длину номера карты
    if len(card_number) != 16:
        logger.error("Номер карты должен содержать 16 цифр.")
        raise ValueError("Номер карты должен содержать 16 цифр.")

    # Маскируем номер карты
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    logger.info(f"Успешно замаскирован номер карты: {masked_number}")
    return masked_number


def get_mask_account(account_number: str) -> str:
    # Проверяем номер на наличие только цифр и минимальную длину
    if not account_number.isdigit() or len(account_number) < 4:
        logger.error("Номер счета должен содержать только цифры и иметь минимум 4 цифры.")
        raise ValueError("Номер счета должен содержать только цифры и иметь минимум 4 цифры.")

    # Маскируем номер счета
    masked_account_number = f"**{account_number[-4:]}"

    logger.info(f"Успешно замаскирован номер счета: {masked_account_number}")
    return masked_account_number


# Примеры использования функций
try:
    print(get_mask_card_number("1234 5678 9012 3456"))
except ValueError as e:
    logger.error(f"Ошибка: {e}")

try:
    print(get_mask_account("123456789"))
except ValueError as e:
    logger.error(f"Ошибка: {e}")
