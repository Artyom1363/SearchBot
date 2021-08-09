from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types

import handler_sentences
import record

def request(sentence, USER_ID_TELEG, cursor, connection, bot, type_content = 0):

    fl = handler_sentences.insert_qust_with_answere(sentence, 
        USER_ID_TELEG, connection, cursor, type_content)
    
    if not fl:
        bot.send_message(USER_ID_TELEG, "error")
        return

    change_state_query = f"UPDATE users SET state = 'search' "\
                         f"WHERE id = {USER_ID_TELEG};"
    cursor.execute(change_state_query)
    connection.commit()

    #menu = record.Menu()
    #menu.print(bot, USER_ID_TELEG, 
    bot.send_message(USER_ID_TELEG, 
        text = "Спасибо, мы приняли ваш ответ, вы в меню!\nВведите запрос:",
        )
    
