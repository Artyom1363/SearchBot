from getpass import getpass
from mysql.connector import connect, Error

from telebot import types
import telebot

import record

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


                change_state_query = f"UPDATE users SET state = 'start' "\
                                     f"WHERE id = {USER_ID_TELEG};"
                cursor.execute(change_state_query)
                connection.commit()


                got_sentences_id = handler_sentences.search_sentence(message.text, 
                    CONNECTION_DB, limit = 3)
                
                rec = record.Record(got_sentences_id)
                rec.print(bot, CONNECTION_DB, USER_ID_TELEG)


                
                

    except Error as e:
        print(e)
