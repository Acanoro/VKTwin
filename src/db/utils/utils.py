import os

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_env_file_path():
    """
    Возвращает путь к файлу .env.

    :return: Путь к файлу .env или None, если файл не найден.
    """
    try:
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_root_dir = os.path.abspath(os.path.join(current_file_dir, '..', '..', '..', ))
        env_file_path = os.path.join(project_root_dir, '.env')

        if not os.path.exists(env_file_path):
            logger.error(f"Файл .env не найден по пути: {env_file_path}")
            return None

        return env_file_path
    except Exception as e:
        logger.error(f"Ошибка при получении пути к файлу .env: {e}")
        return None
