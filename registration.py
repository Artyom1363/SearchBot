import telebot
from telebot import types

import record
import config


def register_user(USER_ID_TELEG, user_name, cursor, connection, bot):
    test_query = f"SELECT count(1) FROM users " \
                 f"WHERE id = {USER_ID_TELEG};"

    cursor.execute(test_query)
    result = cursor.fetchall()
    if result[0][0] == 0:
        state = 'search'
        insert_query = f"INSERT INTO users (state, name, id) " \
                       f"VALUES ('{state}', '{user_name}', {USER_ID_TELEG} );"

        cursor.execute(insert_query)
        connection.commit()

    # отправка user_guide
    bot.send_message(USER_ID_TELEG,
                     text='Пожалуйста, потратьте 30 секунд и ознакомьтесь с Руководством пользователя:')
    bot.send_document(USER_ID_TELEG, config.USER_GUIDE)
    bot.send_video(USER_ID_TELEG, config.VIDEO_GUIDE)
    bot.send_message(USER_ID_TELEG, text='Введите запрос:')
