from getpass import getpass
from mysql.connector import connect, Error
import telebot
from telebot import types


def get_user_state(message, cursor, connection):
    """
    function returns state of user who sent this message

    """
    
    USER_ID_TELEG = message.chat.id
    test_query = f"SELECT state FROM users "\
                f"WHERE id = {USER_ID_TELEG};"

    cursor.execute(test_query)
    result = cursor.fetchall()

    if len(result) == 0:
    	return ""

    return result[0][0]
