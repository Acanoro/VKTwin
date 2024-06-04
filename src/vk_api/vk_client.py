import requests
import logging

from dotenv import dotenv_values

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

secrets = dotenv_values(".env")


class VKAPI:
    """
    Класс для взаимодействия с API ВКонтакте.
    """
    API_BASE_URL = 'https://api.vk.com/method/'
    DEFAULT_VERSION = '5.236'

    def __init__(self, token=None, version=None):
        self.__token = secrets['VK_TOKEN']
        self.__version = version or self.DEFAULT_VERSION
        self.__params = {'access_token': self.__token, 'v': self.__version}

    def _build_url(self, api_method):
        """
        Строит URL для API-запроса.

        :param api_method: Метод API.
        :return: Полный URL для запроса.
        """
        return f"{self.API_BASE_URL}/{api_method}"

    def _make_request(self, method, params=None):
        """
        Выполняет HTTP-запрос к API ВКонтакте.

        :param method: Метод API.
        :param params: Параметры запроса.
        :return: Ответ от сервера в формате JSON.
        """
        try:
            response = requests.get(self._build_url(method), params={**self.__params, **params})
            response.raise_for_status()
            logger.info(f"Запрос {method} успешно выполнен")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Ошибка при выполнении запроса {method}: {e}")
            return None

    def _get_popular_photos(self, owner_id, count=3):
        """
        Получает список популярных фотографий пользователя.

        :param count: Количество фотографий для получения.
        :return: Фотографии пользователя в формате JSON.
        """
        params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'count': count,
            'extended': 1,
            'sort': 'likes_desc'
        }
        return self._make_request("photos.get", params=params)

    def _get_city_id(self, city_name):
        """
        Получает идентификатор города по его названию.

        :param city_name: Название города.
        :return: Идентификатор города или None, если город не найден.
        """
        params = {'q': city_name, 'count': 1, 'need_all': 0}
        response = self._make_request("database.getCities", params=params)

        if response and 'response' in response and 'items' in response['response']:
            items = response['response']['items']
            if items:
                return items[0]['id']
        logger.error(f"Город '{city_name}' не найден")
        return None

    def _get_user_data(self, user):
        """
        Формирует данные о пользователе, включая популярные фотографии.

        :param user: Объект пользователя.
        :return: Данные о пользователе в формате JSON.
        """
        try:
            user_data = {
                'user_id': user['id'],
                'user_link': f'https://vk.com/id{user["id"]}',
                'last_name': user['last_name'],
                'first_name': user['first_name'],
                'photos': []
            }

            popular_photos = self._get_popular_photos(user['id'])

            if popular_photos and 'response' in popular_photos and 'items' in popular_photos['response']:
                for photo in popular_photos['response']['items']:
                    user_data['photos'].append(photo['sizes'][-1]['url'])

            return user_data
        except KeyError as e:
            logger.error(f"Отсутствует ключ в данных пользователя: {e}")
            return None

    def get_users_info(self, id_user):
        """
        Получает информацию о пользователе.

        :return: Информация о пользователе в формате JSON.
        """
        params = {'user_ids': id_user}

        user = self._make_request("users.get", params=params)

        if user and 'response' in user and user['response']:
            try:
                user_data = self._get_user_data(user['response'][0])
                return user_data
            except IndexError:
                logger.error("Пользователь с данным ID не найден")
                return None
        else:
            logger.error("Ошибка при получении информации о пользователе")
            return None

    def search_users(self, age_from, age_to, sex, city, offset):
        """
        Получает список пользователей по возрасту, полу и городу.

        :param age_from: Минимальный возраст пользователя.
        :param age_to: Максимальный возраст пользователя.
        :param sex: Пол пользователя (1 — женский; 2 — мужской; 0 — любой).
        :param city: Название города пользователя.
        :param offset: Смещение относительно первой найденной записи.
        :return: Список пользователей в формате JSON.
        """
        params = {
            'city': self._get_city_id(city),
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
            'count': 1,
            'offset': offset,
            'has_photo': 1,
        }

        user = self._make_request("users.search", params=params)

        if user and 'response' in user and 'items' in user['response'] and user['response']['items']:
            user_data = self._get_user_data(user['response']['items'][0])
            return user_data
        return None
