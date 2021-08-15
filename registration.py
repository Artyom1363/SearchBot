import telebot
from telebot import types

import record


def register_user(USER_ID_TELEG, user_name, cursor, connection, bot):
    
    test_query = f"SELECT count(1) FROM users "\
                f"WHERE id = {USER_ID_TELEG};"
    
    cursor.execute(test_query)
    result = cursor.fetchall()
    if result[0][0] == 0:

        state = 'search'
        insert_query = f"INSERT INTO users (state, name, id) " \
        f"VALUES ('{state}', '{user_name}', {USER_ID_TELEG} );"

        cursor.execute(insert_query)
        connection.commit()

    #отправка user_guide
    bot.send_message(USER_ID_TELEG, 
        text = 'Пожалуйста, потратьте 30 секунд и ознакомьтесь в Руководством пользователя:')
    bot.send_document(USER_ID_TELEG, 
        'BQACAgIAAxkBAAIHF2EUAZ4nUM_C04JaQJHy7iA76qpAAALGEQAC1pWhSKuQ535Ac65jIAQ')
    bot.send_message(USER_ID_TELEG, text = 'Введите запрос:')


