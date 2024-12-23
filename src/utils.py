import json
import logging
import os

# Создаем папку logs, если она не существует
if not os.path.exists('logs'):
    os.makedirs('logs')

# Настройка логирования
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logs/utils.log')
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


def read_transactions_from_json(file_path: str):
    """
    Читает транзакции из JSON-файла.

    :param file_path: Путь к JSON-файлу.
    :return: Список словарей с данными о финансовых транзакциях.
    """
    # Получаем абсолютный путь к файлу
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = os.path.join(BASE_DIR, "data", file_path)

    if not os.path.exists(absolute_path):
        logger.error(f"Файл не найден: {absolute_path}")
        return []

    with open(absolute_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                logger.info("Успешно прочитаны данные из JSON.")
                return data
            else:
                logger.warning("Содержимое файла не является списком.")
                return []
        except json.JSONDecodeError:
            logger.error("Ошибка декодирования JSON.")
            return []


# Пример использования функции
file_path = 'operations.json'  # Относительный путь к файлу
transactions = read_transactions_from_json(file_path)
print(transactions)
