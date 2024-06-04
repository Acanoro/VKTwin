import logging

from src.bot.bot_constants import MyStates
from src.bot.views.handle_menu import menu
from src.db.data_handler import create_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_name(bot, message):
    try:
        chat_id = message.chat.id
        full_name = message.text.strip()

        if " " not in full_name:
            bot.send_message(chat_id, "Пожалуйста, введите фамилию и имя через пробел. Пример: Иванов Иван")
            return

        surname, given_name = full_name.split(" ", 1)

        user_data = {'step': MyStates.ASKING_CITY, 'surname': surname, 'given_name': given_name}
        bot.set_state(message.from_user.id, user_data, chat_id)

        bot.send_message(chat_id, "Спасибо! Теперь укажите ваш город:")
    except Exception as e:
        logger.error(f"Ошибка при обработке ввода имени пользователя: {e}")


def handle_city(bot, message):
    try:
        chat_id = message.chat.id
        city = message.text.strip()

        user_data = bot.get_state(message.from_user.id, chat_id)
        if not isinstance(user_data, dict):
            user_data = {}

        user_data['step'] = MyStates.ASKING_AGE
        user_data['city'] = city
        bot.set_state(message.from_user.id, user_data, chat_id)

        bot.send_message(chat_id, "Спасибо! Теперь укажите ваш возраст:")
    except Exception as e:
        logger.error(f"Ошибка при обработке ввода города пользователя: {e}")


def handle_age(bot, message):
    try:
        chat_id = message.chat.id
        age = message.text.strip()

        if not age.isdigit() or not 0 <= int(age) <= 100:
            bot.send_message(chat_id, "Пожалуйста, введите настоящий возраст (от 0 до 100).")
            return

        user_data = bot.get_state(message.from_user.id, chat_id)
        if not isinstance(user_data, dict):
            user_data = {}

        user_data['step'] = MyStates.ASKING_GENDER
        user_data['age'] = age
        bot.set_state(message.from_user.id, user_data, chat_id)

        bot.send_message(chat_id, "Отлично! Пожалуйста, укажите ваш пол ('м' для мужского, 'ж' для женского):")
    except Exception as e:
        logger.error(f"Ошибка при обработке ввода возраста пользователя: {e}")


def handle_gender(bot, message):
    try:
        chat_id = message.chat.id
        gender = message.text.strip().lower()

        if gender not in ['м', 'ж']:
            bot.send_message(chat_id, "Пожалуйста, укажите ваш пол как 'м' (мужской) или 'ж' (женский).")
            return

        user_data = bot.get_state(message.from_user.id, chat_id)
        if not isinstance(user_data, dict):
            user_data = {}

        surname = user_data.get('surname')
        given_name = user_data.get('given_name')
        city = user_data.get('city')
        age = int(user_data.get('age', 0))

        create_user(id_tg=message.from_user.id, first_name=given_name, last_name=surname, city=city, age=age,
                    gender=gender)

        bot.set_state(message.from_user.id, None, chat_id)

        bot.send_message(chat_id, "Регистрация завершена! Вот ваше меню:")

        menu(bot, message)
    except Exception as e:
        logger.error(f"Ошибка при обработке ввода пола пользователя: {e}")
