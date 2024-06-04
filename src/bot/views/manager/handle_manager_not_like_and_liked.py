from src.bot.utils.utils import get_and_send_user_info_liked_list, get_and_send_user_info_block_list
from src.db.data_handler import get_user_by_id_tg, remove_from_favorites, remove_from_blacklist


def handle_back_user(bot, message):
    chat_id = message.chat.id
    id_tg = message.from_user.id

    with bot.retrieve_data(id_tg, chat_id) as data:
        page = data['page_list_not_like_and_liked']
        current_name_page = data['current_page_name']

    if current_name_page == 'handle_list_liked':
        get_and_send_user_info_liked_list(bot, message, page - 1)
    elif current_name_page == 'handle_list_not_like':
        get_and_send_user_info_block_list(bot, message, page - 1)


def handle_next_user(bot, message):
    chat_id = message.chat.id
    id_tg = message.from_user.id

    with bot.retrieve_data(id_tg, chat_id) as data:
        page = data['page_list_not_like_and_liked']
        current_name_page = data['current_page_name']

    if current_name_page == 'handle_list_liked':
        get_and_send_user_info_liked_list(bot, message, page + 1)
    elif current_name_page == 'handle_list_not_like':
        get_and_send_user_info_block_list(bot, message, page + 1)


def handle_delete_user_list(bot, message):
    chat_id = message.chat.id
    id_tg = message.from_user.id

    obj_user = get_user_by_id_tg(id_tg=id_tg)

    with bot.retrieve_data(id_tg, chat_id) as data:
        profile_id = data['profile_id']
        page = data['page_list_not_like_and_liked']
        current_name_page = data['current_page_name']

    if current_name_page == 'handle_list_liked':
        remove_from_favorites(user_id=obj_user.id, profile_id=profile_id)
        get_and_send_user_info_liked_list(bot, message, page)
    elif current_name_page == 'handle_list_not_like':
        remove_from_blacklist(user_id=obj_user.id, profile_id=profile_id)
        get_and_send_user_info_block_list(bot, message, page)
