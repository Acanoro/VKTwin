from src.bot.utils.utils import get_and_send_user_info_block_list, create_like_and_not_like_keyboard


def handle_list_not_like(bot, message):
    chat_id = message.chat.id
    id_tg = message.from_user.id

    with bot.retrieve_data(id_tg, chat_id) as data:
        data['current_page_name'] = 'handle_list_not_like'

    markup = create_like_and_not_like_keyboard()

    bot.send_message(chat_id, "Не понравилось", reply_markup=markup)

    get_and_send_user_info_block_list(bot, message, 0)

