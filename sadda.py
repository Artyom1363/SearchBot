import telebot
from telebot import types
from mysql.connector import Error
import ustate
import sup

import handler_sentences
import record


def request(sentence, USER_ID_TELEG, cursor,
            connection, bot, type_content=0, file_id=''):

    # trying to put user's sentence to database (smileys cant be added to database)
    try:
        fl = handler_sentences.insert_qust_with_answere(sentence, USER_ID_TELEG,
                                                        connection, cursor,
                                                        type_content, file_id)
    except Error as err:
        sup.print_log("unsup symbols sadda.py: " + str(err))
        bot.send_message(chat_id=USER_ID_TELEG,
                         text='Вы используете недопустимые символы, ' \
                              'пожалуйста исправьте запрос')
        return

    if not fl:
        bot.send_message(USER_ID_TELEG, "Произвошла ошибка, попробуйте еще раз")
        return

    ustate.set_state(USER_ID_TELEG, 'search', cursor,
                     connection)

    bot.send_message(USER_ID_TELEG,
                     text='Спасибо, мы приняли ' \
                          'ваш ответ, вы в меню!\n' \
                          'Введите запрос:'
                     )
