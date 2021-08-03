from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types

import handler_sentences

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

                markup = types.ReplyKeyboardMarkup()
                item_search = types.KeyboardButton('Поиск')
                item_find = types.KeyboardButton('Добавить')
                markup.row(item_search, item_find)

                sentence = message.text;
                fl = handler_sentences.insert_answere(sentence, USER_ID_TELEG, CONNECTION_DB)
                
                if not fl:
                    bot.send_message(USER_ID_TELEG, "error", reply_markup = markup)
                    return

                change_state_query = f"UPDATE users SET state = 'start' "\
                                     f"WHERE id = {USER_ID_TELEG};"
                cursor.execute(change_state_query)
                connection.commit()


                bot.send_message(USER_ID_TELEG, "Спасибо, мы приняли ваш ответ, вы в меню!",
                    reply_markup = markup)
                

    except Error as e:
        print(e)
