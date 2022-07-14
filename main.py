from datetime import datetime
import telebot
import os
import sys
import json


with open('sample_phrase.json', encoding='utf8') as json_file:
    data = json.load(json_file)
    wake_up_phrase = data.get('wake_up_phrase')
    token = data.get('token')
    who_to_follow = data.get('who_to_follow')
    id_chat = data.get('id_chat')
    start_time = data.get('start_time')


start_str = datetime.strptime(start_time, "%d/%m/%Y %H:%M:%S")
st_str = start_str.strftime("%d/%m/%Y %H:%M:%S")
connection_file_name = 'sleep_guy.txt'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.username == who_to_follow:
        mess = f'Привет, <b>{message.from_user.username}</b>'
        bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def handle_text(message):
    if message.from_user.username == who_to_follow:
        if not os.path.exists(connection_file_name):
            messa = wake_up_phrase
            bot.send_message(message.chat.id, messa, parse_mode='html')
            with open(connection_file_name, 'w') as ouf:
                ouf.write('Проснулся')
            sys.exit(0)
    pass


if __name__ == '__main__':
    print('Я начинаю работу')
    if os.path.exists(connection_file_name):
        os.remove(connection_file_name)
        print('Я удалил файл')
    else:
        print("Такого файла не существует")
    print('Я начинаю работу')
    bot.polling(none_stop=True, interval=0)
