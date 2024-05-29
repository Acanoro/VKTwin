import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VKAPI:
    """
    Класс для взаимодействия с API ВКонтакте.
    """
    API_BASE_URL = 'https://api.vk.com/method/'
    DEFAULT_VERSION = '5.199'

    def __init__(self, token=None, user_id=None, version=None):
        self.__token = token or input("Введите токен доступа VK: ")
        self.__id = user_id or input("Введите ID пользователя VK: ")
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

    def get_users_info(self):
        """
        Получает информацию о пользователе.

        :return: Информация о пользователе в формате JSON.
        """
        params = {'user_ids': self.__id}
        return self._make_request("users.get", params=params)

    def get_photos(self, count=5):
        """
        Получает фотографии пользователя.

        :param count: Количество фотографий для получения.
        :return: Фотографии пользователя в формате JSON.
        """
        params = {'owner_id': self.__id, 'album_id': 'profile', 'count': count, 'extended': 1}
        return self._make_request("photos.get", params=params)

    def create_photo_dicts(self, photos_data):
        """
        Создает список словарей с информацией о фотографиях.

        :param photos_data: Данные о фотографиях в формате JSON.
        :return: Список словарей с информацией о фотографиях.
        """
        if 'response' in photos_data:
            photos_info = []
            for photo in photos_data['response']['items']:
                info = {
                    'photo': photo['sizes'][-1]['url'],
                    'type': photo['sizes'][-1]['type'],
                    'likes': photo['likes']['count'],
                    'date': photo['date']
                }
                photos_info.append(info)
            return photos_info
        else:
            logger.error("Неверный формат данных при получении фотографий")
            return None

    def get_user_photos_info(self, count=5):
        """
        Получает информацию о фотографиях пользователя.

        :param count: Количество фотографий для получения.
        :return: Информация о фотографиях пользователя в формате словаря.
        """
        photos_data = self.get_photos(count=count)
        if photos_data:
            logger.info("Фотографии успешно получены")
            return self.create_photo_dicts(photos_data)
        else:
            return None
