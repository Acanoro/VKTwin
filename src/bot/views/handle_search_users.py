from telebot import types

from src.bot.bot_constants import Command
from src.bot.utils.utils import search_and_send_user
from src.db.data_handler import get_user_by_id_tg, get_profile_by_vk_id, add_profile, get_blacklisted_profiles, \
    add_to_blacklist, get_favorites_profiles, add_to_favorites


def handle_search_users(bot, message):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    did_not_like_btn = types.KeyboardButton(Command.DID_NOT_LIKE)
    liked_btn = types.KeyboardButton(Command.LIKED)
    menu_btn = types.KeyboardButton(Command.MENU)

    markup.add(did_not_like_btn, liked_btn)
    markup.add(menu_btn)

    bot.send_message(chat_id, "Поиск пользователей", reply_markup=markup)

    search_and_send_user(bot=bot, message=message, offset=0)


def handle_reaction(bot, message, reaction_type):
    chat_id = message.chat.id
    id_tg = message.from_user.id

    with bot.retrieve_data(id_tg, chat_id) as data:
        id_user_vk = data['id_user_vk']
        offset_search = data['offset_search']

    obj_user = get_user_by_id_tg(id_tg=id_tg)

    obj_profile_by_vk_id = get_profile_by_vk_id(vk_id=id_user_vk)

    if not obj_profile_by_vk_id:
        obj_profile_by_vk_id = add_profile(vk_id=id_user_vk)

    added_to_list = add_to_reaction_list(obj_user, obj_profile_by_vk_id, reaction_type)

    if added_to_list:
        search_and_send_user(bot=bot, message=message, offset=offset_search + 1)


def add_to_reaction_list(obj_user, obj_profile, reaction_type):
    if reaction_type == 'did_not_like':
        if not get_blacklisted_profiles(user_id=obj_user.id, profile_id=obj_profile.id):
            add_to_blacklist(user_id=obj_user.id, profile_id=obj_profile.id)
        return True
    elif reaction_type == 'liked':
        if not get_favorites_profiles(user_id=obj_user.id, profile_id=obj_profile.id):
            add_to_favorites(user_id=obj_user.id, profile_id=obj_profile.id)
        return True
    return False


def handle_did_not_like(bot, message):
    handle_reaction(bot, message, 'did_not_like')


def handle_liked(bot, message):
    handle_reaction(bot, message, 'liked')
