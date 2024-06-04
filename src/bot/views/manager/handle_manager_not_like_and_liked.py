import logging

from src.bot.utils.utils import get_and_send_user_info_liked_list, get_and_send_user_info_block_list
from src.db.data_handler import get_user_by_id_tg, remove_from_favorites, remove_from_blacklist, \
    get_blacklisted_profiles, get_favorites_profiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_back_user(bot, message):
    """
    Обрабатывает команду "Назад" пользователя при просмотре списка понравившихся или непонравившихся профилей.

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

        with bot.retrieve_data(id_tg, chat_id) as data:
            page = data.get('page_list_not_like_and_liked')
            current_name_page = data.get('current_page_name')

        if current_name_page == 'handle_list_liked':
            obj_favorites = get_favorites_profiles(user_id=obj_user.id)

            if obj_favorites:
                get_and_send_user_info_liked_list(bot, message, page - 1)
        elif current_name_page == 'handle_list_not_like':
            obj_black_list = get_blacklisted_profiles(user_id=obj_user.id)

            if obj_black_list:
                get_and_send_user_info_block_list(bot, message, page - 1)
    except Exception as e:
        logger.error(f"Ошибка при обработке команды 'handle_back_user': {e}")


def handle_next_user(bot, message):
    """
    Обрабатывает команду "Далее" пользователя при просмотре списка понравившихся или непонравившихся профилей.

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

        with bot.retrieve_data(id_tg, chat_id) as data:
            page = data.get('page_list_not_like_and_liked')
            current_name_page = data.get('current_page_name')

        if current_name_page == 'handle_list_liked':
            obj_favorites = get_favorites_profiles(user_id=obj_user.id)

            if obj_favorites:
                get_and_send_user_info_liked_list(bot, message, page + 1)
        elif current_name_page == 'handle_list_not_like':
            obj_black_list = get_blacklisted_profiles(user_id=obj_user.id)

            if obj_black_list:
                get_and_send_user_info_block_list(bot, message, page + 1)
    except Exception as e:
        logger.error(f"Ошибка при обработке команды 'handle_next_user': {e}")


def handle_delete_user_list(bot, message):
    """
    Обрабатывает команду "Удалить" пользователя при просмотре списка понравившихся или непонравившихся профилей.

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

        with bot.retrieve_data(id_tg, chat_id) as data:
            profile_id = data.get('profile_id')
            page = data.get('page_list_not_like_and_liked')
            current_name_page = data.get('current_page_name')

        if current_name_page == 'handle_list_liked':
            obj_favorites = get_favorites_profiles(user_id=obj_user.id)

            if obj_favorites:
                remove_from_favorites(user_id=obj_user.id, profile_id=profile_id)
                get_and_send_user_info_liked_list(bot, message, page)
        elif current_name_page == 'handle_list_not_like':
            obj_black_list = get_blacklisted_profiles(user_id=obj_user.id)

            if obj_black_list:
                remove_from_blacklist(user_id=obj_user.id, profile_id=profile_id)
                get_and_send_user_info_block_list(bot, message, page)
    except Exception as e:
        logger.error(f"Ошибка при обработке команды 'handle_delete_user_list': {e}")
