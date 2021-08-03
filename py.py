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


#class with variables for connecting to db
CONNECTION_DB = config.ConnectionDb()

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    #bot.send_message(message.chat.id, '_', reply_markup = types.ReplyKeyboardRemove())
    #return
    registration.register_user(message, CONNECTION_DB, bot)



@bot.message_handler(func=lambda m: True)
def echo_all(message):
    state = ustate.get_user_state(message, CONNECTION_DB)
    print(state)
    if state == 'start':
        sstart.request(message, CONNECTION_DB, bot)

    if state == 'search_sentence':
        ssearch.request(message, CONNECTION_DB, bot)

    if state == 'adding_sentence':
        sadds.request(message, CONNECTION_DB, bot)

    if state == 'adding_answere':
        sadda.request(message, CONNECTION_DB, bot)
	#handler_sentences.search_sentence(message.text, CONNECTION_DB)
	#markup = types.ReplyKeyboardMarkup()
	#item_search = types.KeyboardButton('you want to add a question')
	#item_find = types.KeyboardButton('you want to find a question')
	#markup.row(item_search, item_find)
	#got_sentences = handler_sentences.search_sentence(message.text, CONNECTION_DB)
	#if len(got_sentences) > 0:
		#bot.send_message(message.chat.id, got_sentences[0])



bot.polling()
