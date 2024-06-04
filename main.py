from telebot import TeleBot, StateMemoryStorage

from dotenv import dotenv_values
import logging

from src.bot.register_handlers import register_handlers
from src.db.database import conn_db

# from db.database import conn_db
# from handlers.register_handlers import register_handlers
# from logger_config import setup_logging

secrets = dotenv_values(".env")


def main():
    """
    Основная функция запуска бота.
    """
    # try:
    # setup_logging()
    conn_db(create_tables_flag=True)
    state_storage = StateMemoryStorage()
    bot = TeleBot('7018655405:AAFfqYl7f0W0nYIfoer0EtENptLUhsvEbtY', state_storage=state_storage)
    register_handlers(bot)
    bot.polling()
    # except Exception as e:
    #     logging.error(f"An error occurred: {e}")


if __name__ == '__main__':
    logging.info('Starting the bot...')
    main()
