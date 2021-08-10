from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types

import handler_sentences

def get_markup_cancell():
    cancell = types.InlineKeyboardButton(text = 'отмена', 
            callback_data = f'cancell')

    markup = types.InlineKeyboardMarkup()
    markup.add(cancell)
    return markup

def request(settings, cursor, connection, ans_id = -1, sentence = ''):

    USER_ID_TELEG, message_id, CONNECTION_DB, bot = settings
    if ans_id == -1 and sentence == '':
        fl = True
    elif ans_id != -1:
        fl = insert_by_answere_id(ans_id, connection, cursor, settings)

    else:
        fl = insert_by_question(sentence, connection, cursor, settings)

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
        "Напишите ответ или загрузите файл", 
        reply_markup = get_markup_cancell())
                

def insert_by_answere_id(ans_id, connection, cursor, settings):
    get_sentence_id_query = f"SELECT sentence_id FROM answeres "\
                            f"WHERE id = {ans_id};"
    cursor.execute(get_sentence_id_query)
    result = cursor.fetchall()
    if len(result) == 0:
        return False

    return handler_sentences.insert_sentence_to_user(str('@&388&__&__' + str(result[0][0])), 
        settings[0], 
        connection, 
        cursor)


def insert_by_question(sentence, connection, cursor, settings):
    return handler_sentences.insert_sentence_to_user(sentence, 
        settings[0], 
        connection, 
        cursor)

