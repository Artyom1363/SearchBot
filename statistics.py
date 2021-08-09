from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types


def get_result(query, cursor):
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        return result[0][0]
    else:
        return 'None'

def get_quantity_of_own_answeres(USER_ID_TELEG, cursor):
    get_quantity_of_ans_query = f"SELECT count(1) FROM answeres " \
                                f"WHERE user_id = {USER_ID_TELEG};"
    return get_result(get_quantity_of_ans_query, cursor)

def get_quantity_of_own_likes(USER_ID_TELEG, cursor):
    get_quantity_of_likes_query = f"SELECT count(1) FROM users_liked_answeres " \
                                      f"WHERE user_id = {USER_ID_TELEG};"
    return get_result(get_quantity_of_likes_query, cursor)

def get_quantity_of_users(cursor):
    get_q_of_users_query = f"SELECT count(1) FROM users;"
    return get_result(get_q_of_users_query, cursor)

def get_q_of_ans(cursor):
    get_q_of_ans_query = f"SELECT count(1) FROM answeres;"
    return get_result(get_q_of_ans_query, cursor)

def get_q_of_likes(cursor):
    get_q_of_likes_query = f"SELECT count(1) FROM users_liked_answeres;"
    return get_result(get_q_of_likes_query, cursor)

def get_q_of_ques(cursor):
    get_q_of_ques_query = f"SELECT count(1) FROM sentences;"
    return get_result(get_q_of_ques_query, cursor)

def print_statistics(settings):
    USER_ID_TELEG, message_id, CONNECTION_DB, bot = settings
    try:
        with connect(
            host = CONNECTION_DB.HOST,
            user = CONNECTION_DB.USER,
            password = CONNECTION_DB.PASSWORD,
            database = CONNECTION_DB.DATABASE
        ) as connection:
            with connection.cursor() as cursor:
                q_sents = get_quantity_of_own_answeres(USER_ID_TELEG, 
                        cursor)
                q_likes = get_quantity_of_own_likes(USER_ID_TELEG, cursor)
                statistics = f"Кол-во моих 📥: {q_sents}\n"\
                             f"Кол-во моих ❤️: {q_likes}\n"

                if str(USER_ID_TELEG) == '556001234':
                    q_u = get_quantity_of_users(cursor)
                    q_ans = get_q_of_ans(cursor)
                    q_likes = get_q_of_likes(cursor)
                    q_ques = get_q_of_ques(cursor)
                    statistics += f"Кол-во 🧍‍♂: {q_u}\n" \
                                  f"Кол-во 📥 :{q_ans}\n" \
                                  f"Кол-во ❤️: {q_likes}\n" \
                                  f"Кол-во ❓: {q_ques}\n"

                bot.send_message(USER_ID_TELEG,  
                    statistics
                    )

    except Error as e:
        print(e)