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
#DEBUG
import action
test_link_file = ''

#class with variables for connecting to db
CONNECTION_DB = config.ConnectionDb()

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    #bot.send_message(message.chat.id, '_', 
    #reply_markup = types.ReplyKeyboardRemove())
    #return
    registration.register_user(message, CONNECTION_DB, bot)


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):

    settings = [call.message.chat.id, 
                call.message.message_id, 
                CONNECTION_DB, 
                bot]

    print(call.data)
    data = call.data.split(sep = '_')
    print(data)
    if data[0] == 'file':
        #print(data[2])
        print(call.data)
        hash_file = record.get_hash(CONNECTION_DB, data[1])
        bot.send_document(call.message.chat.id, hash_file)

    if data[0] == 'question':
        t = record.Comment(settings)
        t.print_comment_rec_id(data[1])

    if data[0] == 'soon':
    	t = record.Comment(settings)
    	t.next_comment(data[1])
        #record.next(data[1], settings)
    if data[0] == 'back':
        t = record.Comment(settings)
        t.prev_comment(data[1])
        #record.next(data[1], settings)

    if call.data == 'поиск':
        sstart.request(call.data, call.message.chat.id, CONNECTION_DB, bot)

    if call.data == 'добавить':
        sstart.request(call.data, call.message.chat.id, CONNECTION_DB, bot)

    #obj = record.Record(130)
    #obj.edit_and_send(call.message.chat.id, call.message.message_id, bot)



    #bot.delete_message(call.message.chat.id, call.message.message_id)
    '''print('\n\n\n\n')
    print(type(call))
    print(dir(call), end = '\n\n')
    print('data: ', call.data, end = '\n\n')
    print('from_user type: ', type(call.from_user))
    print('call.from_user: ', call.from_user, end = '\n\n')
    print('id: ', call.id, end = '\n\n')
    print('inline_message_id: ', call.inline_message_id, end = '\n\n')
    print('message', call.message, end = '\n\n')'''


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    #test_link_file = str(test_link_file)
    #print(test_link_file)
    #bot.send_document(message.chat.id, 'BQACAgIAAxkBAAIC8WENG1FvuIPa045NBUJTAAHRiODi1wAC3g0AArfuaUi7XrxwpHP4xSAE')
    #return
    

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
        #bot.delete_message(message.chat.id, message.message_id)
        #menu = record.Menu()
        #menu.print(bot, message.chat.id)

    if state == 'search_sentence':
        ssearch.request(message, CONNECTION_DB, bot)

    if state == 'adding_sentence':
        sadds.request(message.text, message.chat.id, CONNECTION_DB, bot)

    if state == 'adding_answere':
        sadda.request(message.text, message.chat.id, CONNECTION_DB, bot)
    #handler_sentences.search_sentence(message.text, CONNECTION_DB)
    #markup = types.ReplyKeyboardMarkup()
    #item_search = types.KeyboardButton('you want to add a question')
    #item_find = types.KeyboardButton('you want to find a question')
    #markup.row(item_search, item_find)
    #got_sentences = handler_sentences.search_sentence(message.text, CONNECTION_DB)
    #if len(got_sentences) > 0:
        #bot.send_message(message.chat.id, got_sentences[0])

@bot.message_handler(content_types=['document'])
def handle_docs_document(message):
    state = ustate.get_user_state(message, CONNECTION_DB)

    if state == 'adding_answere':
        sadda.request(message.document.file_id, message.chat.id, CONNECTION_DB, bot, type_content = 1)

    test_link_file = message.document.file_id
    print(message.document.file_id)


bot.polling()

