from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types

import handler_sentences

def request(sentence, USER_ID_TELEG, CONNECTION_DB, bot):
    """
    

    """
    #id of user in telegram
    
    try:
        with connect(
            host = CONNECTION_DB.HOST,
            user = CONNECTION_DB.USER,
            password = CONNECTION_DB.PASSWORD,
            database = CONNECTION_DB.DATABASE
        ) as connection:
            with connection.cursor() as cursor:

                fl = handler_sentences.insert_sentence(sentence, 
                    USER_ID_TELEG, 
                    CONNECTION_DB)

                if not fl:
                    #TASK: ADD INFO
                    bot.send_message(USER_ID_TELEG, "error", 
                        reply_markup = types.ReplyKeyboardRemove())
                    return

                change_state_query = f"UPDATE users SET state = 'adding_answere' "\
                                     f"WHERE id = {USER_ID_TELEG};"
                cursor.execute(change_state_query)
                connection.commit()


                bot.send_message(USER_ID_TELEG, 
                    "Укажите ответ на этот вопрос", 
                    reply_markup = types.ReplyKeyboardRemove())
                

    except Error as e:
        print(e)

