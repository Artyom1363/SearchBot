from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types


def get_user_state(message, CONNECTION_DB):
    """
    function returns state of user who sent this message

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
                test_query = f"SELECT state FROM users "\
                            f"WHERE id = {USER_ID_TELEG};"
                
                cursor.execute(test_query)
                result = cursor.fetchall()

                if len(result) == 0:
                	return ""

                return result[0][0]

    except Error as e:
        print(e)
