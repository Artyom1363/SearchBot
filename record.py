from telebot import types
import time

import sup

import handler_sentences

import likes


class Record:
    def __init__(self, rec_ids, settings, button_back=False):
        self.rec_ids = rec_ids
        self.button_back = button_back
        try:
            self.USER_ID_TELEG = settings[0]
            self.message_id = settings[1]
            self.CONNECTION_DB = settings[2]
            self.bot = settings[3]
        except IndexError as ie:
            print(ie)

    def print(self, cursor, connection):

        markup = types.InlineKeyboardMarkup()

        for record_id in self.rec_ids:
            sen = handler_sentences.get_sentence_by_id(
                record_id, cursor, connection)
            button = types.InlineKeyboardButton(text=sen,
                                                callback_data=f'question_{record_id}')
            markup.add(button)

        button = types.InlineKeyboardButton(
            text="Добавить ответ на свой вопрос📥",
            callback_data=f'addSame')

        markup.add(button)

        letter = ''
        if len(self.rec_ids) > 0:
            letter = "Вот что нам удалось найти:\n"


        else:
            letter = "По вашему запросу ничего не найдено\n"

        # start = time.time()
        if self.button_back:
            self.bot.edit_message_text(message_id=self.message_id,
                                       chat_id=self.USER_ID_TELEG,
                                       text=letter,
                                       reply_markup=markup,
                                       parse_mode='Markdown')
        else:
            self.bot.send_message(self.USER_ID_TELEG,
                                  letter,
                                  reply_markup=markup,
                                  parse_mode='Markdown')


class Comment:

    def __init__(self, settings, call_id='0'):
        try:
            self.USER_ID_TELEG = settings[0]
            self.message_id = settings[1]
            self.bot = settings[3]
        except IndexError as ie:
            print(ie)
        self.call_id = call_id

    def make_markup_comment(self, comment_id, text, likes_info, type_content=0):

        if type_content == 1:
            comment = types.InlineKeyboardButton(
                text=f'{text}\n✉️',
                callback_data=f'file_{comment_id}')
        elif type_content == 2:
            comment = types.InlineKeyboardButton(
                text=f'{text}\n✉️',
                callback_data=f'photo_{comment_id}')
        else:
            comment = types.InlineKeyboardButton(text=text,
                                                 callback_data=f'none')

        before = types.InlineKeyboardButton(text='⬅️',
                                            callback_data=f'prev_{comment_id}')

        if likes_info[1] == 0:
            like_expose = str(likes_info[0]) + " ♡"
        else:
            like_expose = str(likes_info[0]) + " ❤️"

        like = types.InlineKeyboardButton(text=like_expose,
                                          callback_data=f'like_{comment_id}')

        add = types.InlineKeyboardButton(text='📥',
                                         callback_data=f'add_{comment_id}')
        after = types.InlineKeyboardButton(text='➡️',
                                           callback_data=f'next_{comment_id}')

        exit = types.InlineKeyboardButton(text='назад',
                                          callback_data=f'back_{comment_id}')

        first_row = [before, like, add, after]
        markup = types.InlineKeyboardMarkup(row_width=4)
        markup.add(comment)
        markup.add(*first_row)
        markup.add(exit)
        return markup

    def print_comment_rec_id(self, record_id, cursor, connection):
        start = time.time()

        get_comment_query = f"SELECT id, ans_text, type FROM " \
                            f"answeres WHERE sentence_id = '{record_id}' " \
                            f"order by likes DESC, id DESC LIMIT 1;"
        cursor.execute(get_comment_query)
        sen = cursor.fetchall()

        self.print_comment(sen[0][0], sen[0][1],
                           sen[0][2], cursor, connection)

    def print_comment_ans_id(self, ans_id, cursor, connection):
        get_comment_query = f"SELECT ans_text, type FROM " \
                            f"answeres WHERE id = '{ans_id}' LIMIT 1;"
        cursor.execute(get_comment_query)
        sen = cursor.fetchall()

        self.print_comment(ans_id, sen[0][0],
                           sen[0][1], cursor, connection)

    def print_comment(self, ans_id, ans_text, type_content, cursor, connection):

        likes_info = likes.get_likes(self.USER_ID_TELEG,
                                     ans_id, cursor, connection)

        markup = self.make_markup_comment(ans_id,
                                          ans_text, likes_info, type_content=type_content)

        sentence_id = handler_sentences.get_sentence_id_by_ans_id(ans_id,
                                                                  cursor, connection)

        sentence = handler_sentences.get_sentence_by_id(sentence_id,
                                                        cursor, connection)
        try:
            self.bot.edit_message_text(chat_id=self.USER_ID_TELEG,
                                       message_id=self.message_id,
                                       text=f'Сейчас вы видите комментарии пользователей на вопрос: *{sentence}*',
                                       reply_markup=markup,
                                       parse_mode='Markdown')
        except:
            sup.print_log('message have already modified!')

    def get_all_comments_id(self, ans_id, cursor, connection):
        sen_id = handler_sentences.get_sentence_id_by_ans_id(
            ans_id, cursor, connection)

        answers_id_query = f"SELECT id FROM " \
                           f"answeres WHERE sentence_id = '{sen_id}' " \
                           f"order by likes DESC, id DESC;"
        cursor.execute(answers_id_query)
        ids_cort = cursor.fetchall()
        ids = [id_cort[0] for id_cort in ids_cort]

        return ids

    def next_comment(self, ans_id, cursor, connection):
        ans_id = int(ans_id)
        ids = self.get_all_comments_id(ans_id, cursor, connection)
        upper_id = get_upper_id(ans_id, ids)
        if upper_id is None:

            self.bot.answer_callback_query(self.call_id,
                                           text='Вы смотрите последний комментарий!',
                                           show_alert=True)
        else:
            self.print_comment_ans_id(upper_id, cursor, connection)

    def prev_comment(self, ans_id, cursor, connection):
        ans_id = int(ans_id)
        ids = self.get_all_comments_id(ans_id, cursor, connection)
        lower_id = get_lower_id(ans_id, ids)
        if lower_id is None:

            self.bot.answer_callback_query(self.call_id,
                                           text='Вы смотрите первый комментарий',
                                           show_alert=True)
        else:
            self.print_comment_ans_id(lower_id, cursor, connection)

    def like(self, ans_id, cursor, connection):
        likes.make_like(self.USER_ID_TELEG, ans_id, cursor, connection)
        self.print_comment_ans_id(ans_id, cursor, connection)


def get_hash(ans_id, cursor, connection):
    get_comment_query = f"SELECT file_id FROM " \
                        f"answeres WHERE id = '{ans_id}' LIMIT 1;"
    cursor.execute(get_comment_query)
    sen = cursor.fetchall()
    if len(sen) > 0:
        return sen[0][0]
    else:
        return ''


def get_upper_id(elem, lst):
    for i in range(len(lst)):
        if lst[i] == elem:
            if i + 1 < len(lst):
                return lst[i + 1]
            else:
                return None
    return None


def get_lower_id(elem, lst):
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == elem:
            if i - 1 >= 0:
                return lst[i - 1]

            else:
                return None
    return None
