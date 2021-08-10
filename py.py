import telebot
import config
from telebot import types

from mysql.connector import connect, Error


#importing modules needed to handle requests 
import handler_sentences
import registration
import ustate

#importing moduls needed to handle user's state
import ssearch
import sadds
import sadda


import record
import statistics

#DEBUG
import action
import time

#class with variables for connecting to db
CONNECTION_DB = config.ConnectionDb()

bot = telebot.TeleBot(config.TOKEN)

def func_throw_db(func, message):
    start = time.time()
    try:
        with connect(
            host = CONNECTION_DB.HOST,
            user = CONNECTION_DB.USER,
            password = CONNECTION_DB.PASSWORD,
            database = CONNECTION_DB.DATABASE
        ) as connection:
            with connection.cursor() as cursor:
                func(message, cursor, connection)

    except Error as e:
        print(e)	
    print('py.py time of execution is: ', time.time() - start)


@bot.message_handler(commands=['info'])
def send_welcome(message):
    start = time.time()
    settings = [message.chat.id, 
                message.message_id, 
                CONNECTION_DB, 
                bot]

    bot.send_message(message.chat.id, 'Ваша статистика:')
    statistics.print_statistics(settings)
    print("time of execution: ", time.time() - start, " seconds\n")
    

@bot.message_handler(commands=['start'])
def send_welcome(message):
    registration.register_user(message, CONNECTION_DB, bot)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
	func_throw_db(test_callback, call)

@bot.message_handler(func=lambda m: True)
def text_handler(message):
	func_throw_db(text_message, message)

@bot.message_handler(content_types=['document'])
def doc_handler(message):
	func_throw_db(handle_docs_document, message)

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
	func_throw_db(handle_photo_document, message)


def test_callback(call, cursor, connection):
    start = time.time()

    settings = [call.message.chat.id, 
                call.message.message_id, 
                CONNECTION_DB, 
                bot]

    new_settings = [call.message.chat.id, 
                    call.message.message_id, 
                    cursor,
                    connection, 
                    bot]

    data = call.data.split(sep = '_')
    print(data)
    if data[0] == 'like':
        t = record.Comment(settings)
        t.like(data[1], cursor, connection)
    if data[0] == 'cancell':
    	ustate.set_search_state(call.message.chat.id, cursor, connection)
    	bot.delete_message(call.message.chat.id, call.message.message_id)

    if data[0] == 'back':
        ssearch.request(call.data, settings, cursor, connection, True)

    if data[0] == 'file':
        hash_file = record.get_hash(data[1], 
            cursor, connection)
        bot.send_document(call.message.chat.id, hash_file)

    if data[0] == 'photo':
        hash_file = record.get_hash(data[1],
            cursor, connection)
        bot.send_photo(call.message.chat.id, hash_file)

    if data[0] == 'question':
        t = record.Comment(settings)
        t.print_comment_rec_id(data[1], cursor, connection)

    if data[0] == 'next':
        t = record.Comment(settings)
        t.next_comment(data[1], cursor, connection)

    if data[0] == 'prev':
        t = record.Comment(settings)
        t.prev_comment(data[1], cursor, connection)

    if data[0] == 'add':
        sadds.request(settings, cursor, connection, ans_id = data[1])

    if data[0] == 'addSame':
        sadds.request(settings, cursor, connection)
        bot.delete_message(call.message.chat.id, call.message.message_id)



def text_message(message, cursor, connection):
    settings = [message.chat.id, 
                message.message_id, 
                CONNECTION_DB, 
                bot]
    

    if message.text == 't':
        bot.delete_message(message.chat.id, message.message_id)
        action.test(bot, message)
        return

    state = ustate.get_user_state(message, cursor, connection)

    print(state, message.text)
    if state == 'search':
        ssearch.request(message.text, settings, cursor, connection)

    if state == 'adding_sentence':
        sadds.request(settings, cursor, connection, sentence = message.text)

    if state == 'adding_answere':
        sadda.request(message.text, message.chat.id, cursor, connection, bot)



def handle_docs_document(message, cursor, connection):
    #print(message.text)
    #print("message: ", (message))
    #print('caption: ', message.caption)
    state = ustate.get_user_state(message, cursor, connection)
    file_id = message.document.file_id

    if state == 'adding_answere':
        sadda.request(message.caption, message.chat.id, 
            cursor, connection, bot, 1, file_id)



def handle_photo_document(message, cursor, connection):
    #print(message.text)
    #print('caption: ', message.caption)
    file_id = message.photo[2].file_id
    state = ustate.get_user_state(message, cursor, connection)

    if state == 'adding_answere':
        sadda.request(message.caption, message.chat.id, 
            cursor, connection, bot, 2, file_id)


bot.polling()


