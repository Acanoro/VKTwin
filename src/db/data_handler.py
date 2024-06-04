from src.db.database import conn_db
from src.db.models import *


def create_user(**kwargs) -> Users:
    """
    Создает нового пользователя в базе данных.

    :param kwargs: Параметры пользователя.
    :return: Объект пользователя.
    """

    session, engine = conn_db()
    user = Users(**kwargs)
    session.add(user)
    session.commit()
    session.close()
    return user


def get_user_by_id_tg(id_tg: int) -> Users:
    """
    Получает пользователя по его ID Telegram из базы данных.

    :param id_tg: ID Telegram пользователя.
    :return: Объект пользователя.
    """

    session, engine = conn_db()
    user = session.query(Users).filter(Users.id_tg == id_tg).first()
    session.close()
    return user


def add_profile(vk_id: int) -> profiles:
    """
    Добавляет профиль в базу данных.

    :param vk_id: ID профиля VK.
    :return: Объект профиля.
    """
    session, engine = conn_db()
    profile_entry = profiles(vk_id=vk_id)
    session.add(profile_entry)
    session.commit()

    profile_entry = session.query(profiles).get(profile_entry.id)

    session.close()

    return profile_entry


def get_profile_by_vk_id(vk_id: int) -> profiles:
    """
    Получает профиль по его VK ID.

    :param vk_id: ID профиля VK.
    :return: Объект профиля.
    """
    session, engine = conn_db()
    profile = session.query(profiles).filter(profiles.vk_id == vk_id).first()
    session.close()
    return profile


def get_profile_by_id(id: int) -> profiles:
    """
    Получает профиль по его VK ID.

    :param vk_id: ID профиля VK.
    :return: Объект профиля.
    """
    session, engine = conn_db()
    profile = session.query(profiles).filter(profiles.id == id).first()
    session.close()
    return profile


def add_to_blacklist(user_id: int, profile_id: int) -> BlackList:
    """
    Добавляет профиль в черный список пользователя и возвращает объект черного списка.

    :param user_id: ID пользователя.
    :param profile_id: ID профиля.
    :return: Объект черного списка.
    """
    session, engine = conn_db()
    blacklist_entry = BlackList(user_id=user_id, profile_id=profile_id)
    session.add(blacklist_entry)
    session.commit()
    session.close()
    return blacklist_entry


def remove_from_blacklist(user_id: int, profile_id: int) -> None:
    """
    Удаляет профиль из черного списка пользователя.

    :param user_id: ID пользователя.
    :param profile_id: ID профиля.
    """
    session, engine = conn_db()

    blacklist_entry = session.query(BlackList).filter_by(user_id=user_id, profile_id=profile_id).first()

    session.delete(blacklist_entry)
    session.commit()

    session.close()


def get_blacklisted_profiles(user_id: int, profile_id: int = None) -> list[BlackList]:
    """
    Получает все профили в черном списке для заданного пользователя.
    Если указан profile_id, фильтрует также по нему.

    :param user_id: ID пользователя.
    :param profile_id: (опционально) ID профиля.
    :return: Список объектов черного списка.
    """

    session, engine = conn_db()
    if user_id and profile_id:
        query = session.query(BlackList).filter(
            (BlackList.user_id == user_id) & (BlackList.profile_id == profile_id)
        ).all()
    else:
        query = session.query(BlackList).filter(BlackList.user_id == user_id).all()

    session.close()
    return query


def add_to_favorites(user_id: int, profile_id: int) -> BlackList:
    """
    Добавляет профиль в черный список пользователя и возвращает объект черного списка.

    :param user_id: ID пользователя.
    :param profile_id: ID профиля.
    :return: Объект черного списка.
    """
    session, engine = conn_db()
    favorites_entry = favorites(user_id=user_id, profile_id=profile_id)
    session.add(favorites_entry)
    session.commit()
    session.close()
    return favorites_entry


def get_favorites_profiles(user_id: int, profile_id: int = None) -> list[BlackList]:
    """
    Получает все профили в черном списке для заданного пользователя.
    Если указан profile_id, фильтрует также по нему.

    :param user_id: ID пользователя.
    :param profile_id: (опционально) ID профиля.
    :return: Список объектов черного списка.
    """
    session, engine = conn_db()
    if user_id and profile_id:
        query = session.query(favorites).filter(
            (favorites.user_id == user_id) & (favorites.profile_id == profile_id)
        ).all()
    else:
        query = session.query(favorites).filter(favorites.user_id == user_id).all()

    session.close()
    return query


def remove_from_favorites(user_id: int, profile_id: int) -> None:
    """
    Удаляет профиль из черного списка пользователя.

    :param user_id: ID пользователя.
    :param profile_id: ID профиля.
    """
    session, engine = conn_db()

    favorites_entry = session.query(favorites).filter_by(user_id=user_id, profile_id=profile_id).first()

    session.delete(favorites_entry)
    session.commit()

    session.close()
