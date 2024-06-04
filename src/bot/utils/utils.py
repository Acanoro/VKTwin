from telebot import types

from src.bot.bot_constants import Command
from src.db.data_handler import get_user_by_id_tg, get_blacklisted_profiles, get_profile_by_id, get_favorites_profiles, \
    get_profile_by_vk_id
from src.vk_api.vk_client import VKAPI


def create_menu_keyboard():
    """
    Создает клавиатуру для основного меню бота.

    :return: Объект клавиатуры.
    """
    search_btn = types.KeyboardButton(Command.Search)
    did_not_like_btn = types.KeyboardButton(Command.BLACK_LIST)
    liked_btn = types.KeyboardButton(Command.LIKE_LIST)

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(search_btn)
    markup.add(did_not_like_btn, liked_btn)

    return markup


def create_like_and_not_like_keyboard():
    """
    Создает клавиатуру для основного меню бота.

    :return: Объект клавиатуры.
    """
    back_btn = types.KeyboardButton(Command.BACK)
    next_btn = types.KeyboardButton(Command.NEXT)
    del_not_liked_btn = types.KeyboardButton(Command.DELETE_USER_LIST)
    menu_btn = types.KeyboardButton(Command.MENU)

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(back_btn, next_btn)
    markup.add(del_not_liked_btn)
    markup.add(menu_btn)

    return markup


def send_user_media_group(bot, chat_id, search_user):
    if search_user:
        user_message = f"Имя: {search_user['first_name']} {search_user['last_name']}\n"
        user_message += f"Ссылка на профиль: {search_user['user_link']}"

        attachments = search_user['photos']

        media = [
            types.InputMediaPhoto(photo, caption=user_message if i == 0 else '') for i, photo in enumerate(attachments)
        ]

        bot.send_media_group(chat_id, media)
    else:
        bot.send_message(chat_id, "Не удалось найти пользователей по заданным критериям.")


def search_and_send_user(bot, message, offset):
    chat_id = message.chat.id
    id_tg = message.from_user.id

    user = get_user_by_id_tg(id_tg=id_tg)
    obj_favorites = [obj_favorite.profile_id for obj_favorite in get_favorites_profiles(user_id=user.id)]
    obj_black_list = [obj_black_list.profile_id for obj_black_list in get_blacklisted_profiles(user_id=user.id)]

    sex = '1' if user.gender == 'м' else '2'

    vk_api = VKAPI()

    search_user = None
    photos_bool = False
    while not photos_bool:
        search_user = vk_api.search_users(
            age_from=user.age - 2,
            age_to=user.age + 1,
            sex=sex,
            city=user.city,
            offset=offset
        )

        if search_user is None:
            continue

        obj_profiles = get_profile_by_vk_id(vk_id=search_user['user_id'])
        if search_user['photos'] and not obj_profiles:
            if obj_profiles and (obj_profiles.id not in obj_favorites and obj_profiles.id not in obj_black_list):
                photos_bool = True
            else:
                photos_bool = True
        else:
            offset += 1

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['id_user_vk'] = search_user['user_id']
        data['offset_search'] = offset

    send_user_media_group(bot, chat_id, search_user)


def get_and_send_user_info(bot, message, page, get_profiles_func):
    chat_id = message.chat.id
    id_tg = message.from_user.id

    obj_user = get_user_by_id_tg(id_tg=id_tg)
    obj_profiles_list = get_profiles_func(user_id=obj_user.id)

    if not obj_profiles_list:
        bot.send_message(chat_id, "Список пользователей пуст.")
        return

    if page < 0:
        page = len(obj_profiles_list) - 1
    elif page > len(obj_profiles_list) - 1:
        page = 0

    obj_profile = get_profile_by_id(id=obj_profiles_list[page].profile_id)

    vk_api = VKAPI()
    search_user = vk_api.get_users_info(id_user=obj_profile.vk_id)

    with bot.retrieve_data(id_tg, chat_id) as data:
        data['page_list_not_like_and_liked'] = page
        data['profile_id'] = obj_profiles_list[page].profile_id

    send_user_media_group(bot, chat_id, search_user)


def get_and_send_user_info_block_list(bot, message, page):
    get_and_send_user_info(bot, message, page, get_blacklisted_profiles)


def get_and_send_user_info_liked_list(bot, message, page):
    get_and_send_user_info(bot, message, page, get_favorites_profiles)
