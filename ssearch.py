from telebot import types
from mysql.connector import Error
import telebot

import sup

import record
import config

import handler_sentences


def request(sentence, settings, cursor, connection, button_back=False):

    USER_ID_TELEG, message_id, CONNECTION_DB, bot = settings

    if not button_back:

        # trying to put user's sentence to database (smileys cant be added to database)
        try:
            handler_sentences.insert_sentence_to_user(sentence,
                                                      USER_ID_TELEG, connection, cursor)
        except Error as err:
            sup.print_log("unsup symbols: " + str(err))
            bot.send_message(chat_id=USER_ID_TELEG,
                             text='Вы используете недопустимые символы, ' \
                                  'пожалуйста исправьте запрос')
            return

    else:
        get_sentence_query = f"SELECT sentences FROM users " \
                             f"WHERE id = {USER_ID_TELEG};"

        cursor.execute(get_sentence_query)
        result = cursor.fetchall()

        if len(result) == 0:
            sup.print_log('error in search.py : len(result) = 0')
            return

        sentence = result[0][0]
        data = sentence.split(config.toSplit)

        # case if user already tried to put answer to some question
        # (then we put to db number of question but not user's question itself)
        if data[0] == config.firstPart:
            try:
                bot.edit_message_text(chat_id=USER_ID_TELEG,
                                      message_id=message_id,
                                      text='Сейчас вы можете продолжить поиск:')
            except:
                sup.print_log('message have already modified!')

            return

    got_sentences_id = handler_sentences.search_sentence(sentence,
                                                         cursor, connection, limit=5)

    rec = record.Record(got_sentences_id, settings, button_back)
    rec.print(cursor, connection)
