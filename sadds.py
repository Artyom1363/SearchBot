from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types
import config
import ustate

import handler_sentences

def get_markup_cancell():
    cancell = types.InlineKeyboardButton(text = 'отмена', 
            callback_data = f'cancell')

    markup = types.InlineKeyboardMarkup()
    markup.add(cancell)
    return markup

def request(settings, cursor, connection, ans_id = -1, sentence = ''):

    USER_ID_TELEG, message_id, CONNECTION_DB, bot = settings
    fl = False
    mes_to_user = ''
    if ans_id == -1 and sentence == '':
        fl = True

        #make message
        sentence = handler_sentences.get_sentence_from_users(
            USER_ID_TELEG, connection, cursor)
        mes_to_user = f"Вы добавляете ответ на вопрос: *{sentence}*"
        
    elif ans_id != -1:
        #make message
        sen_id = handler_sentences.get_sentence_id_by_ans_id(ans_id, 
            cursor, connection)
        sentence = handler_sentences.get_sentence_by_id(
            sen_id, cursor, connection)
        mes_to_user = f"Добавьте ответ к вопросу *{sentence}*"

        #make fl
        fl = insert_by_answere_id(ans_id, connection, cursor, settings)
    

    if not fl:
        bot.send_message(USER_ID_TELEG, "error", 
            reply_markup = types.ReplyKeyboardRemove())
        return


    ustate.set_state(USER_ID_TELEG, 'adding_answere', cursor, 
        connection)


    bot.send_message(USER_ID_TELEG, 
        mes_to_user, 
        reply_markup = get_markup_cancell(), 
        parse_mode= 'Markdown')
                

def insert_by_answere_id(ans_id, connection, cursor, settings):
    sen_id = handler_sentences.get_sentence_id_by_ans_id(ans_id, 
        cursor, connection)

    return handler_sentences.insert_sentence_to_user(str('@&388&__&__' + str(sen_id)), 
        settings[0], 
        connection, 
        cursor)


def get_sentence_id_by_ans_id(ans_id, cursor, connection):
    get_sentence_id_query = f"SELECT sentence_id FROM answeres "\
                            f"WHERE id = {ans_id};"
    cursor.execute(get_sentence_id_query)
    result = cursor.fetchall()
    if len(result) == 0:
        return False

    return result[0][0]


def insert_by_question(sentence, connection, cursor, settings):
    return handler_sentences.insert_sentence_to_user(sentence, 
        settings[0], 
        connection, 
        cursor)

