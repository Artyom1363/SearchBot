from getpass import getpass
from mysql.connector import connect, Error

from telebot import types
import telebot

import record
import config

import handler_sentences

def request(sentence, settings, cursor, connection, button_back = False):

    USER_ID_TELEG, message_id, CONNECTION_DB, bot = settings

    if not button_back:

        handler_sentences.insert_sentence_to_user(sentence, 
            USER_ID_TELEG, connection, cursor)

    else:
        get_sentence_query = f"SELECT sentences FROM users " \
                             f"WHERE id = {USER_ID_TELEG};"

        cursor.execute(get_sentence_query)
        result = cursor.fetchall()

        if len(result) == 0:
            print('error in search.py : len(result) = 0')
            return

        sentence = result[0][0]
        data = sentence.split(config.toSplit)
        if data[0] == config.firstPart:
            bot.edit_message_text(chat_id = USER_ID_TELEG, 
                message_id = message_id, 
                text = 'Сейчас вы можете продолжить поиск:')
            return


    got_sentences_id = handler_sentences.search_sentence(sentence, 
        CONNECTION_DB, limit = 5)

    rec = record.Record(got_sentences_id, settings, button_back)
    rec.print()

