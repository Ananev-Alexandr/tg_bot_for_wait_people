import schedule
import time
import telebot
import sys
import os
from datetime import datetime
import pymorphy2
import json


with open('sample_phrase.json', encoding='utf8') as json_file:
    data = json.load(json_file)
    wait_phrase = data.get('wait_phrase')
    finish_phrase = data.get('finish_phrase')
    token = data.get('token')
    start_time = data.get('start_time')
    id_chat = data.get('id_chat')


bot = telebot.TeleBot(token)
connection_file_name = 'sleep_guy.txt'


def creat_time_str(delta, base_str, if_last=False):
    days = delta.days
    hours = (delta.seconds - days) // 3600
    minutes = (delta.seconds - days - hours * 3600) // 60
    seconds = (delta.seconds - days - hours * 3600 - minutes * 60)
    morph = pymorphy2.MorphAnalyzer()
    if days:
        word = morph.parse('день')[0]
        a = word.make_agree_with_number(days).word
        base_str = base_str + f' {days}{a}'
    if hours:
        word = morph.parse('час')[0]
        a = word.make_agree_with_number(hours).word
        base_str = base_str + f' {hours}{a}'
    if minutes:
        word = morph.parse('минуту')[0]
        a = word.make_agree_with_number(minutes).word
        base_str = base_str + f' {minutes}{a}'
    if seconds:
        word = morph.parse('секунду')[0]
        a = word.make_agree_with_number(seconds).word
        base_str = base_str + f' {seconds}{a}'
    return base_str


def job():
    now = datetime.now()
    start_datetime = datetime.strptime(start_time, "%d/%m/%Y %H:%M:%S")
    delta = now - start_datetime
    base_str = wait_phrase
    result_string = creat_time_str(delta, base_str)
    bot.send_message(chat_id=id_chat, text=result_string, parse_mode='html')
    print('Я отправил сообщение пользователю')


def job2():
    if os.path.exists(connection_file_name):
        now = datetime.now()
        start_datetime = datetime.strptime(start_time, "%d/%m/%Y %H:%M:%S")
        delta = now - start_datetime
        base_str = finish_phrase
        result_string = creat_time_str(delta, base_str)
        bot.send_message(chat_id=id_chat, text=result_string, parse_mode='html')
        print('Я завершаю работу')
        sys.exit(0)


schedule.every(5).seconds.do(job)
schedule.every(1).seconds.do(job2)

while True:
    schedule.run_pending()
    time.sleep(1)
