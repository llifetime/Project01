import logging


def setup_logger(name, log_file, level=logging.INFO):
    """Настройка логгера для модуля"""

    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Формат сообщения
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Обработчик для записи в файл (перезаписывает файл при каждом запуске)
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger


# Инициализация логгеров для модулей
masks_logger = setup_logger('masks', 'logs/masks.log')
utils_logger = setup_logger('utils', 'logs/utils.log')
