import datetime


def print_log(log):
    with open('log.txt', 'a') as f:
        f.write(str(datetime.datetime.now()) + "  " + str(log) + "\n")


def print_call_log(call):
    log = f"{call.message.chat.id} " \
          f"call.data: {call.data}"
    print_log(log)


def mess_log(message):
    log = f"{message.chat.id} " \
          f"text: {message.text}"
    print_log(log)


def photo_log(message):
    log = f"{message.chat.id}, photo_id: {message.photo[2].file_id}"
    print_log(log)


def doc_log(message):
    log = f"{message.chat.id}, doc_id: {message.document.file_id}"
    print_log(log)


'''
def print_f(*args):
	output = open('log.txt', 'a')
	now = datetime.datetime.now()
	output.write(str(now))
	output.write(' ')
	for arg in args:
		output.write(str(arg))
		output.write(' ')
	output.write('\n')
	output.close()
'''
