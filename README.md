# VKTwin

VKTwin - это бот для платформы Телеграм, предназначенный для помощи пользователям в поиске знакомств. Он предлагает
различные варианты людей для знакомств в виде диалога с пользователем, предоставляя удобный интерфейс для взаимодействия
и управления списками понравившихся и не понравившихся пользователей.

## Оглавление

- [Описание проекта](#описание-проекта)
- [Решаемые проблемы](#решаемые-проблемы)
- [Используемый стек технологий](#используемый-стек-технологий)
- [Установка](#установка)
- [Использование](#использование)
- [Конфигурация](#конфигурация)
- [Документация](#Документация)
- [Схема бд](#Схема-бд)
- [Структура проекта](#структура-проекта)
- [Вклад](#вклад)
- [Лицензия](#лицензия)

## Описание проекта

VKTwin автоматизирует процесс знакомства в социальной сети ВКонтакте. Пользователи могут зарегистрироваться, искать
потенциальных партнеров, оценивать их и управлять своими списками понравившихся и не понравившихся пользователей. Бот
предоставляет удобный и интуитивно понятный интерфейс для взаимодействия в виде диалога.

## Решаемые проблемы

- **Упрощение процесса знакомства**: автоматизация поиска и оценки потенциальных партнеров.
- **Экономия времени**: пользователи могут быстро находить подходящих партнеров без необходимости тратить много времени
  на ручной поиск.
- **Удобство**: предоставление удобного интерфейса для управления списками пользователей.

## Используемый стек технологий

- **Язык программирования**: Python
- **Фреймворк для бота**: TeleBot
- **База данных**: PostgreSQL
- **API**: ВКонтакте API
- **Логирование**: Python Logging

## Установка

Для запуска проекта VKTwin вам потребуется выполнить следующие шаги:

1. Установка Python

   Если у вас еще не установлен Python, следуйте инструкциям на официальном
   сайте: [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. Установка PostgreSQL

   Для работы с базой данных вам также понадобится PostgreSQL. Вы можете загрузить его с официального
   сайта: [https://www.postgresql.org/download/](https://www.postgresql.org/download/).

3. Клонирование репозитория или создание форка

   Вы можете клонировать основной репозиторий проекта VKTwin или создать форк для собственной работы. Для клонирования
   выполните следующую команду:

```bash
git clone https://github.com/Acanoro/VKTwin.git
```

4. Установка зависимостей

   Перейдите в каталог с проектом и установите необходимые зависимости с помощью `pip`:

```bash
cd VKTwin
pip install -r requirements.txt
```

После выполнения этих шагов вы будете готовы к запуску проекта VKTwin.

## Использование

1. Запустите бота:

    ```bash
    python src/main.py
    ```

2. Бот начнет работу и будет готов к взаимодействию с пользователями ВКонтакте.

## Конфигурация

Конфигурационные параметры проекта находятся в файле `.env`.

Пример файла `.env`:

```dotenv
USER=
PASSWORD=
NAME=
HOST=
PORT=

VK_TOKEN=
TG_TOKEN=
```

`TG_TOKEN`: токен вашего бота tg.

`VK_TOKEN`: токен вашего бота vk.

`USER`, `PASSWORD`, `NAME`, `HOST`, `PORT`: данные для подключения к базе данных.

## Документация

Подробная документация по установке, настройке и использованию проекта доступна в директории `docs/`.

- [Основная документация](docs/index.md)
- [Инструкция по установке](docs/installation.md)
- [Инструкция по использованию](docs/usage.md)

## Структура проекта

```
VKTwin/            # Корневая директория проекта
│
├── src/                  # Директория с исходным кодом проекта
│   ├── bot/              # Модуль, связанный с логикой бота
|   |   ├── utils/
|   |   |   ├── __init__.py
|   │   │   └── utils.py  # Утилиты
|   |   ├── views/
|   |   |   ├── manager/
|   |   |   |   ├── __init__.py
|   |   │   │   └── handle_manager_not_like_and_liked.py  # Обработка списка не понравившихся и понравившихся пользователей
|   |   |   ├── __init__.py
|   │   │   ├── handle_list_did_not_like.py # Обработка списка пользователей, которые не понравились
|   │   │   ├── handle_list_liked.py # Обработка списка пользователей, которые понравились
|   │   │   ├── handle_menu.py # Обработка меню
|   │   │   ├── handle_registration.py # Обработка регистрации пользователя
|   │   │   ├── handle_search_users.py # Обработка поиска пользователей
|   │   │   └── handle_start.py  # Обработка команды /start
│   │   ├── __init__.py   # Инициализационный файл модуля
│   │   ├── bot_constants.py # Константы для бота
│   │   └── register_handlers.py # Регистрация обработчиков команд и событий 
│   │
│   ├── db/               # Модуль для работы с базой данных
|   |   ├── utils/
|   |   |   ├── __init__.py
|   │   │   └── utils.py  # Утилиты
│   │   ├── __init__.py   # Инициализационный файл модуля
│   │   ├── data_handler.py    # Обработка данных
│   │   ├── database.py      # Подключение к базе данных и выполнение определенных операций
│   │   └── models.py        # Определение моделей данных (таблиц базы данных)
│   │
│   ├── vk_api/           # Модуль для взаимодействия с API ВКонтакте
|   |   ├── utils/
|   |   |   ├── __init__.py
|   │   │   └── utils.py  # Утилиты
│   │   ├── __init__.py   # Инициализационный файл модуля
│   │   └── vk_client.py  # Класс клиента для работы с VK API
│
├── tests/                # Директория с тестами
│   ├── test_bot.py       # Тесты для логики бота
│   ├── test_db.py        # Тесты для работы с базой данных
│   ├── test_vk_api.py    # Тесты для взаимодействия с VK API
│   └── test_integration.py # Интеграционные тесты для проверки взаимодействия компонентов
│
├── .env                  # Файл для хранения переменных окружения
├── requirements.txt      # Файл со списком зависимостей проекта
├── README.md             # Основной файл README с описанием проекта
└── .gitignore            # Файл для исключения из контроля версий ненужных файлов    
```

## Схема бд

![img_1.png](img_1.png)

## Вклад

Мы приветствуем вклад сообщества! Пожалуйста, следуйте этим шагам, чтобы внести свой вклад:

1. Сделайте форк репозитория.
2. Создайте новую ветку (`git checkout -b название_вашей_ветки`).
3. Сделайте коммит изменений (`git commit -am 'Добавить какое-то улучшение'`).
4. Отправьте изменения в вашу ветку (`git push origin название_вашей_ветки`).
5. Создайте Pull Request.

## Лицензия

Этот проект лицензирован под лицензией MIT. Подробности см. в файле LICENSE.
