from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types


import handler_sentences

def request(message, CONNECTION_DB, bot):
    """
    

    """

    #id of user in telegram
    USER_ID_TELEG = message.chat.id
    
    try:
        with connect(
            host = CONNECTION_DB.HOST,
            user = CONNECTION_DB.USER,
            password = CONNECTION_DB.PASSWORD,
            database = CONNECTION_DB.DATABASE
        ) as connection:
            with connection.cursor() as cursor:

                markup = types.ReplyKeyboardMarkup()
                item_search = types.KeyboardButton('Поиск')
                item_find = types.KeyboardButton('Добавить')
                markup.row(item_search, item_find)


                change_state_query = f"UPDATE users SET state = 'start' "\
                                     f"WHERE id = {USER_ID_TELEG};"
                cursor.execute(change_state_query)
                connection.commit()


                got_sentences = handler_sentences.search_sentence(message.text, CONNECTION_DB)

                letter = ''
                if len(got_sentences) > 0:
                    if type(got_sentences[0][0]) == str:
                        letter += f"Похожий вопрос, который удалось найти: *{got_sentences[0][0]}*\n"
                    else:
                        letter += f"Произошла ошибка, пожалуйста напишите мне: @htppkt\n"

                    if type(got_sentences[0][1]) == str:
                        letter += f"Ответ на него:*{got_sentences[0][1]}*\n"
                    else:
                        letter += f"К сожалению, на этот вопрос еще не был дан ответ\n"
                else:
                    letter = "По вашему запросу ничего не найдено\n"

                letter += '\n\nВы в меню!'
                bot.send_message(USER_ID_TELEG, letter,
                        reply_markup = markup, parse_mode= 'Markdown')

                
                

    except Error as e:
        print(e)
