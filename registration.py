from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types


def register_user(message, CONNECTION_DB, bot):
    """

    task: we need to print info about user's state

    """
    user_name = message.chat.username

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
                test_query = f"SELECT count(1) FROM users "\
                            f"WHERE id = {USER_ID_TELEG};"
                
                cursor.execute(test_query)
                result = cursor.fetchall()
                if result[0][0] == 0:

               	    state = 'start'
                    insert_query = f"INSERT INTO users (state, name, id) " \
                    f"VALUES ('{state}', '{user_name}', {USER_ID_TELEG} );"

                    cursor.execute(insert_query)
                    connection.commit()

                    inviting = 'Привет, красавица'

                else:
                    inviting = 'Красавица, ты уже зарегистрирована'

                #adding markup
                markup = types.ReplyKeyboardMarkup()
                item_search = types.KeyboardButton('Поиск')
                item_find = types.KeyboardButton('Добавить')
                markup.row(item_search, item_find)

                bot.send_message(message.chat.id, inviting, reply_markup = markup)

    except Error as e:
        print(e)
