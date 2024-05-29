import logging

import sqlalchemy
from dotenv import dotenv_values
from sqlalchemy.orm import sessionmaker

from src.db.models import create_tables
from src.db.utils.utils import get_env_file_path

secrets = dotenv_values(get_env_file_path())


def connect_to_database(DSN: str):
    """
    Подключение к базе данных.

    :param DSN: Строка подключения к базе данных.
    :return: Объект сессии SQLAlchemy и объект движка.
    """
    try:
        engine = sqlalchemy.create_engine(DSN)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session, engine
    except Exception as e:
        logging.error(f"An error occurred while connecting to the database: {e}")
        raise


def conn_db(create_tables_flag: bool = False):
    """
    Подключение к базе данных и выполнение определенных операций.

    :param create_tables_flag: Флаг, указывающий на необходимость создания таблиц.
    :param fill_database_flag: Флаг, указывающий на необходимость заполнения базы данных.
    :return: Объект сессии SQLAlchemy и объект движка.
    """
    user = secrets['USER']
    password = secrets['PASSWORD']
    name = secrets['NAME']
    host = secrets['HOST']
    port = secrets['PORT']

    DSN = f"postgresql://{user}:{password}@{host}:{port}/{name}"

    try:
        session, engine = connect_to_database(DSN)

        if create_tables_flag:
            # создание таблиц
            create_tables(engine)

        return session, engine

    except Exception as e:
        logging.error(f"An error occurred while connecting to the database: {e}")
        raise


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    conn_db()
