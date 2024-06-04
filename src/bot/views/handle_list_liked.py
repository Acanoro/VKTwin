import logging
from src.bot.utils.utils import get_and_send_user_info_liked_list, create_like_and_not_like_keyboard
from src.db.data_handler import get_user_by_id_tg, get_favorites_profiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_list_liked(bot, message):
    """
    Обрабатывает запрос на отображение списка понравившихся профилей пользователю.

    Args:
        bot: Экземпляр бота.
        message: Сообщение от пользователя.

    Returns:
        None
    """
    try:
        chat_id = message.chat.id
        id_tg = message.from_user.id

        obj_user = get_user_by_id_tg(id_tg=id_tg)
        obj_favorites = get_favorites_profiles(user_id=obj_user.id)

        with bot.retrieve_data(id_tg, chat_id) as data:
            data['current_page_name'] = 'handle_list_liked'

        markup = create_like_and_not_like_keyboard()

        if obj_favorites:
            bot.send_message(chat_id, "Понравилось", reply_markup=markup)
            get_and_send_user_info_liked_list(bot, message, 0)
        else:
            bot.send_message(chat_id, "На данный момент список пуст", reply_markup=markup)
    except Exception as e:
        logger.error(f"Ошибка при обработке команды 'handle_list_liked': {e}")