from getpass import getpass
from mysql.connector import connect, Error
import re

import config


def normalize_word(word):
    '''
    function wich normalize word
    task: we need to make compression to "word-word"
    '''

    if type(word) != str:
        return ''
        # raise ValueError(f'expected type str, but {str(type(word))} received')

    word = word.lower()
    pattern = r'[a-zа-я0-9_]+'
    get = re.findall(pattern, word)
    if len(get) > 0:
        return get[0]
    else:
        return ''


def search_sentence(sentence, cursor, connection, limit=5):
    """
    def search_sentence(sentence)
    returns list of most relevants questions
    """
    # print('came')
    sentence = sentence.strip()

    # if sentence too small
    if len(sentence) < 3:
        print(f'expected sentence, with more than 3 symbols but {sentence} received')
        return []

    # spliting our sentence into word
    words_without_handing = sentence.split()

    # key - number of sentence
    # value - quantity of words in 'sentence' which are also in key
    dict_sentence_num = {}

    for word in words_without_handing:

        word = normalize_word(word)
        if len(word) == 0:
            continue

        word_id_query = f"SELECT id FROM words WHERE word = '{word}';"
        cursor.execute(word_id_query)
        result_word_id = cursor.fetchall()

        # if there is not our word in words it make no sence to find this word
        if len(result_word_id) == 0:
            continue

        word_id = result_word_id[0][0]

        # we get all numbers of sentences, which has out word
        sentences_query = f"SELECT sentences_id FROM words_in_sentences " \
                          f"WHERE words_id = {word_id} ;"
        cursor.execute(sentences_query)
        result = cursor.fetchall()

        # fill our dictionary
        for sentence_num in result:
            # sentence_num[0] is 'sentences_id'
            if sentence_num[0] in dict_sentence_num:
                dict_sentence_num[sentence_num[0]] += 1
            else:
                dict_sentence_num[sentence_num[0]] = 1

    # relevance is list with lists like this:
    # [[quantity of occurrence of sentence, number of sentence], ]

    relevance = list()
    for key in dict_sentence_num:
        relevance.append((dict_sentence_num[key], key))

    relevance.sort()
    relevance.reverse()

    # list with selected sentences
    ans = list()

    for i in range(min(limit, len(relevance))):
        # relevance[i][0] is quantity of occurrence of sentence
        # relevance[i][1] is id of sentence
        sentence_id = relevance[i][1]

        # DEBUG
        # print("number of sentence: ", sentence_id, ",
        # quantity of intersections: ", relevance[i][0])

        # sentence_query = f"S sentence, answere from sentences where id =  {sentence_id};"
        # cursor.execute(sentence_query)
        # result = cursor.fetchall()
        # if len(result) == 0:
        # continue

        # adding sentence to answere
        ans.append(sentence_id)

    # insert data to db...as it seems to me...
    connection.commit()
    return ans


def insert_sentence_to_user(sentence, USER_ID_TELEG, connection, cursor):
    sentence = sentence.strip()

    if len(sentence) < 2:
        print("you put too much small string")
        return False

    update_sentence_in_user_query = f"UPDATE users SET sentences = %s " \
                                    f"WHERE id = {USER_ID_TELEG}"

    cursor.execute(update_sentence_in_user_query, (sentence,))
    result = cursor.fetchall()
    connection.commit()
    return True


def get_sentence_from_users(USER_ID_TELEG, connection, cursor):
    get_sentence_from_users_query = f"SELECT sentences FROM users " \
                                    f"WHERE id = {USER_ID_TELEG}"
    cursor.execute(get_sentence_from_users_query)
    result = cursor.fetchall()
    if len(result) == 0:
        return ''
    else:
        return result[0][0]


def insert_sentence(sentence, USER_ID_TELEG, connection, cursor):
    """
    we get string and parse it into words, 
    after we insert all information into database
    """

    sentence = sentence.strip()

    # check sentence
    # if len(sentence) < 3:
    #    print("you put too much small string")
    #   return None
    # raise ValueError('expected sentence, with more than 3 symbols but "' + sentence + '" received')

    # spliting our sentence into words
    words_normalized = [normalize_word(word) for word in sentence.split() if len(normalize_word(word)) > 0]

    # adding original of sentence
    insert_sentence_query = f"INSERT INTO sentences (sentence, len, author_id) " \
                            f"VALUES (%s, {len(words_normalized)}, {USER_ID_TELEG});"
    cursor.execute(insert_sentence_query, (sentence,))

    # getting id of added sentence
    sentence_id = cursor.lastrowid

    # adding words
    for word in words_normalized:

        test_query = f"SELECT id FROM words WHERE word = '{word}' LIMIT 1;"

        cursor.execute(test_query)
        result = cursor.fetchall()

        if (len(result) == 0):
            insert_word_query = f"INSERT INTO words (word) VALUES ('{word}');"
            cursor.execute(insert_word_query)

            word_id = cursor.lastrowid
        else:
            word_id = result[0][0]

        test_query = f"SELECT words_id, sentences_id, count FROM words_in_sentences " \
                     f"WHERE words_id = {word_id} AND sentences_id = {sentence_id} LIMIT 1;"

        cursor.execute(test_query)
        result = cursor.fetchall()

        # for case if we already insert pair {word_id, sentence_id} in our 'for'
        if len(result) == 0:
            insert_query = f"INSERT INTO words_in_sentences (words_id, sentences_id) " \
                           f"VALUES ({word_id}, {sentence_id});"
            cursor.execute(insert_query)
        else:
            update_query = f"UPDATE words_in_sentences SET count = {result[0][2] + 1} " \
                           f"WHERE (words_id = {result[0][0]} AND sentences_id = {result[0][1]});"
            cursor.execute(update_query)

    connection.commit()
    return sentence_id


def insert_qust_with_answere(answere, USER_ID_TELEG,
                             connection, cursor, type_content=0, file_id=''):
    sentence = get_sentence_from_users(USER_ID_TELEG, connection, cursor)
    data = sentence.split(config.toSplit)

    if data[0] == config.firstPart:
        return insert_answere(answere, data[1], USER_ID_TELEG,
                              connection, cursor, type_content, file_id)

    sentence_id = insert_sentence(sentence, USER_ID_TELEG, connection, cursor)
    if sentence_id is None:
        print("ERROR sentence_is is NONE in handler_sentence")

    return insert_answere(answere, sentence_id,
                          USER_ID_TELEG,
                          connection, cursor,
                          type_content, file_id)


def insert_answere(answer, question_id, USER_ID_TELEG,
                   connection, cursor, type_content=0, file_id=''):
    """
    
    """

    # check sentence
    if type(answer) == str and len(answer) > 500:
        print("you put too big string")
        return False

    # adding original of sentence
    if type_content > 0:
        insert_answere_query = f"INSERT INTO answeres (user_id, sentence_id, ans_text, type, file_id) " \
                               f"VALUES ({USER_ID_TELEG}, '{question_id}', %s, {type_content}, '{file_id}')"
    else:
        insert_answere_query = f"INSERT INTO answeres (user_id, sentence_id, ans_text, type) " \
                               f"VALUES ({USER_ID_TELEG}, '{question_id}', %s, {type_content})"

    cursor.execute(insert_answere_query, (answer,))

    connection.commit()
    return True


def get_sentence_by_id(sentence_id, cursor, connection):
    get_sentence_query = f"SELECT sentence FROM sentences " \
                         f"WHERE id = {sentence_id};"
    cursor.execute(get_sentence_query)
    result = cursor.fetchall()
    if len(result) == 0:
        return False

    return result[0][0]


def get_sentence_id_by_ans_id(ans_id, cursor, connection):
    get_sentence_id_query = f"SELECT sentence_id FROM answeres " \
                            f"WHERE id = {ans_id};"
    cursor.execute(get_sentence_id_query)
    result = cursor.fetchall()
    if len(result) == 0:
        return False

    return result[0][0]
