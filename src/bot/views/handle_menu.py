import logging

from src.bot.utils.utils import create_menu_keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def menu(bot, message):
    """
    Отображает меню пользователю.

    Args:
        bot: Экземпляр бота.
        message: Сообщение от пользователя.

    Returns:
        None
    """
    try:
        chat_id = message.chat.id

        markup = create_menu_keyboard()
        bot.send_message(chat_id, "Меню", reply_markup=markup)
    except Exception as e:
        logger.error(f"Ошибка при отображении меню: {e}")
