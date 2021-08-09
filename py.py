import telebot
import config
from telebot import types


#importing modules needed to handle requests 
import handler_sentences
import registration
import ustate

#importing moduls needed to handle user's state
import sstart
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
def test_callback(call):
    start = time.time()

    #DEBUG!
    #bot.send_message(call.message.chat.id, 'test time')
    #print("time of sending message: ", time.time() - start, " seconds\n")
    #!

    settings = [call.message.chat.id, 
                call.message.message_id, 
                CONNECTION_DB, 
                bot]

    data = call.data.split(sep = '_')
    print(data)
    if data[0] == 'like':
        t = record.Comment(settings)
        t.like(data[1])

    if data[0] == 'delete':
    	ssearch.request(call.data, settings, True)

    if data[0] == 'file':
        hash_file = record.get_hash(CONNECTION_DB, data[1])
        bot.send_document(call.message.chat.id, hash_file)

    if data[0] == 'question':
        t = record.Comment(settings)
        t.print_comment_rec_id(data[1])

    if data[0] == 'soon':
    	t = record.Comment(settings)
    	t.next_comment(data[1])

    if data[0] == 'back':
        t = record.Comment(settings)
        t.prev_comment(data[1])

    if data[0] == 'add':
    	sadds.request(settings, ans_id = data[1])

    if data[0] == 'addSame':
        sadds.request(settings)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == 'поиск':
        sstart.request(call.data, call.message.chat.id, CONNECTION_DB, bot)

    if call.data == 'добавить':
        sstart.request(call.data, call.message.chat.id, CONNECTION_DB, bot)


    print("time of execution: ", time.time() - start, " seconds\n")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    start = time.time()
    settings = [message.chat.id, 
                message.message_id, 
                CONNECTION_DB, 
                bot]
    

    if message.text == 't':
        bot.delete_message(message.chat.id, message.message_id)
        action.test(bot, message)
        return

    state = ustate.get_user_state(message, CONNECTION_DB)
    print(state)

    #print('DEBUG: ', state)
    print(state, message.text)
    if state == 'start':
        print(message.text)
        sstart.request(message.text, message.chat.id, CONNECTION_DB, bot)

    if state == 'search':
        ssearch.request(message.text, settings)

    if state == 'adding_sentence':
        sadds.request(settings = settings, sentence = message.text)

    if state == 'adding_answere':
        sadda.request(message.text, message.chat.id, CONNECTION_DB, bot)


    print("py.py time of execution: ", time.time() - start, " seconds\n")

@bot.message_handler(content_types=['document'])
def handle_docs_document(message):
    state = ustate.get_user_state(message, CONNECTION_DB)

    if state == 'adding_answere':
        sadda.request(message.document.file_id, message.chat.id, 
        	CONNECTION_DB, bot, type_content = 1)

    test_link_file = message.document.file_id
    print(message.document.file_id)


bot.polling()

