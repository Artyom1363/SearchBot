from getpass import getpass
from mysql.connector import connect, Error
import re


def get_status_like(USER_ID_TELEG, comment_id, cursor, connection):
    get_status_like_query = f"SELECT count(1) FROM users_liked_answeres " \
                            f"WHERE answere_id = {comment_id} " \
                            f"AND user_id = {USER_ID_TELEG};"
    # print("status in likes.py: ", get_status_like_query)
    cursor.execute(get_status_like_query)
    status_like = cursor.fetchall()
    return status_like[0][0]


def get_quantity_likes(USER_ID_TELEG, comment_id, cursor, connection):
    get_quantity_query = f"SELECT count(1) FROM users_liked_answeres " \
                         f"WHERE answere_id = {comment_id};"
    # print("status in likes.py: ", get_quantity_query)
    cursor.execute(get_quantity_query)
    count_likes = cursor.fetchall()
    return count_likes[0][0]


def get_likes(USER_ID_TELEG, comment_id, cursor, connection):
    count_likes = get_quantity_likes(USER_ID_TELEG, comment_id,
                                     cursor, connection)

    status_like = get_status_like(USER_ID_TELEG, comment_id,
                                  cursor, connection)

    return (count_likes, status_like)


def make_like(USER_ID_TELEG, comment_id, cursor, connection):
    status_like = get_status_like(USER_ID_TELEG, comment_id,
                                  cursor, connection)

    change_like_query = f""
    if int(status_like) > 0:
        change_like_query = f"DELETE FROM users_liked_answeres " \
                            f"WHERE user_id = {USER_ID_TELEG} " \
                            f"AND answere_id = {comment_id};"
    else:
        change_like_query = f"INSERT INTO users_liked_answeres " \
                            f"(user_id, answere_id) " \
                            f"VALUES ({USER_ID_TELEG}, {comment_id});"

    cursor.execute(change_like_query)
    update_likes_in_answeres(USER_ID_TELEG, comment_id,
                             cursor, connection)

    connection.commit()


def update_likes_in_answeres(USER_ID_TELEG, comment_id, cursor, connection):
    count_likes = get_quantity_likes(USER_ID_TELEG, comment_id,
                                     cursor, connection)

    update_likes_query = f"UPDATE answeres SET likes = {count_likes} " \
                         f"WHERE id = {comment_id};"

    cursor.execute(update_likes_query)
    connection.commit()
