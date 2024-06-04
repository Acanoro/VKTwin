from telebot.handler_backends import State, StatesGroup


class Command:
    """
    Класс, содержащий команды бота.
    """
    MENU = 'Меню'
    BLACK_LIST = 'Список не понравилось'
    LIKE_LIST = 'Список понравилось'

    Search = 'Поиск'
    DID_NOT_LIKE = 'Не понравилось'
    LIKED = 'понравилось'

    NEXT = 'Дальше ▶️'
    BACK = 'Назад ◀️'

    DELETE_USER_LIST = 'Удалить пользователя из списка'


class MyStates(StatesGroup):
    """
    Группа состояний бота.
    """
    ASKING_NAME = 'asking_name'
    ASKING_CITY = 'asking_city'
    ASKING_AGE = 'asking_age'
    ASKING_GENDER = 'asking_gender'

    id_user_vk = State()
    offset_search = State()

    page_list_not_like_and_liked = State()
    profile_id = State()

    current_page_name = State()
