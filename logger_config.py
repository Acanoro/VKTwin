import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter


def setup_logging():
    """
    Настройка системы логирования для приложения.

    Создает обработчики для вывода логов в консоль и записи логов в файл 'bot.log'.
    Устанавливает уровень логирования INFO для обоих обработчиков.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = RotatingFileHandler('bot.log', maxBytes=1024000, backupCount=3)
    file_handler.setLevel(logging.INFO)

    console_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


setup_logging()
