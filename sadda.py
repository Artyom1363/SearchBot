import telebot
from telebot import types
import ustate

import handler_sentences
import record


def request(sentence, USER_ID_TELEG, cursor, 
    connection, bot, type_content = 0, file_id = ''):

    fl = handler_sentences.insert_qust_with_answere(sentence, 
        USER_ID_TELEG, connection, cursor, type_content, file_id)
    
    if not fl:
        bot.send_message(USER_ID_TELEG, "error")
        return

    ustate.set_state(USER_ID_TELEG, 'search', cursor, 
        connection)

    bot.send_message(USER_ID_TELEG, 
        text = "Спасибо, мы приняли ваш ответ, вы в меню!\n" \
            "Введите запрос:"
        )
    
