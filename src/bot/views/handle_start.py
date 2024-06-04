import logging

from src.bot.bot_constants import MyStates
from src.bot.views.handle_menu import menu
from src.db.data_handler import get_user_by_id_tg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_start(bot, message):
    """
    Обрабатывает начало диалога с пользователем.

    Args:
        bot: Экземпляр бота.
        message: Сообщение от пользователя.

    Returns:
        None
    """
    chat_id = message.chat.id
    id_tg = message.from_user.id

    try:
        user = get_user_by_id_tg(id_tg=id_tg)

        if user:
            bot.send_message(chat_id, f"С возвращением {user.first_name} {user.last_name}!")

            menu(bot, message)
        else:
            bot.set_state(id_tg, {'step': MyStates.ASKING_NAME}, chat_id)
            bot.send_message(chat_id, "Пожалуйста, введите свою фамилию и имя (через пробел). Пример: Иванов Иван")
    except Exception as e:
        logger.error(f"Ошибка при обработке начала диалога: {e}")
        bot.send_message(chat_id, "Произошла ошибка при обработке вашего запроса. Попробуйте позже.")
