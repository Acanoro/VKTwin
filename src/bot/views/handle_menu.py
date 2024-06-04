from src.bot.utils.utils import create_menu_keyboard


def menu(bot, message):
    """
    Отображает меню пользователю.

    Args:
        bot: Экземпляр бота.
        message: Сообщение от пользователя.

    Returns:
        None
    """
    chat_id = message.chat.id

    markup = create_menu_keyboard()
    bot.send_message(chat_id, "Меню", reply_markup=markup)
