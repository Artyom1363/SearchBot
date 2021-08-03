from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types


def request(message, CONNECTION_DB, bot):
    """
    

    """

    #id of user in telegram
    USER_ID_TELEG = message.chat.id
    
    try:
        with connect(
            host = CONNECTION_DB.HOST,
            user = CONNECTION_DB.USER,
            password = CONNECTION_DB.PASSWORD,
            database = CONNECTION_DB.DATABASE
        ) as connection:
            with connection.cursor() as cursor:
                if message.text == 'Поиск':
                    change_state_query = f"UPDATE users SET state = 'search_sentence' "\
                                         f"WHERE id = {USER_ID_TELEG};"
                    cursor.execute(change_state_query)
                    bot.send_message(USER_ID_TELEG, "Введите запрос", reply_markup = types.ReplyKeyboardRemove())

                elif message.text == 'Добавить':
                    change_state_query = f"UPDATE users SET state = 'adding_sentence' "\
                                         f"WHERE id = {USER_ID_TELEG};"
                    cursor.execute(change_state_query)
                    bot.send_message(USER_ID_TELEG, "Укажите вопрос, "
                        "на который хотите добавить ответ", reply_markup = types.ReplyKeyboardRemove())

                connection.commit()

    except Error as e:
        print(e)