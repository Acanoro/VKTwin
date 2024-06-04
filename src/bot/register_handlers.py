from src.bot.bot_constants import MyStates
from src.bot.views.handle_list_did_not_like import handle_list_not_like
from src.bot.views.handle_list_liked import handle_list_liked
from src.bot.views.handle_menu import menu
from src.bot.views.handle_search_users import handle_search_users, handle_did_not_like, handle_liked
from src.bot.views.handle_start import handle_start
from src.bot.views.handle_registration import handle_name, handle_age, handle_gender, handle_city
from src.bot.views.manager.handle_manager_not_like_and_liked import handle_delete_user_list, handle_back_user, \
    handle_next_user


def register_handlers(bot):
    """
    Регистрирует обработчики сообщений для бота.

    :param bot: Объект бота.
    """
    # Команды
    bot.message_handler(commands=['start'])(lambda message: handle_start(bot, message))

    # Обработчики сообщений для этапов регистрации
    bot.message_handler(func=lambda message: get_current_state(bot, message) == MyStates.ASKING_NAME)(
        lambda message: handle_name(bot, message))
    bot.message_handler(func=lambda message: get_current_state(bot, message) == MyStates.ASKING_CITY)(
        lambda message: handle_city(bot, message))
    bot.message_handler(func=lambda message: get_current_state(bot, message) == MyStates.ASKING_AGE)(
        lambda message: handle_age(bot, message))
    bot.message_handler(func=lambda message: get_current_state(bot, message) == MyStates.ASKING_GENDER)(
        lambda message: handle_gender(bot, message))

    # Текстовые сообщения
    text_handlers = {
        'Меню': menu,
        'Поиск': handle_search_users,
        'Список не понравилось': handle_list_not_like,
        'Список понравилось': handle_list_liked,

        'Не понравилось': handle_did_not_like,
        'понравилось': handle_liked,

        'Назад ◀️': handle_back_user,
        'Дальше ▶️': handle_next_user,

        'Удалить пользователя из списка': handle_delete_user_list,

    }

    for text, handler in text_handlers.items():
        bot.message_handler(
            func=lambda message, text=text: message.text == text
        )(
            lambda message, handler=handler: handler(bot, message)
        )


def get_current_state(bot, message):
    state = bot.get_state(message.from_user.id, message.chat.id)
    if isinstance(state, dict) and 'step' in state:
        return state['step']
    return state
