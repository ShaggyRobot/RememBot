import config
import Scheduler
from date_parse import date_parse

import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove as ReplyKeyboardRemove

bot = telebot.TeleBot(config.token)
handler_STATE = 'init'

markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
buttons = (types.KeyboardButton('10m'),
           types.KeyboardButton('15m'),
           types.KeyboardButton('60m'),
           types.KeyboardButton('Tomorrow'))
markup.add(*buttons)


def send_msg(chat_id: int, text: str, job_name: str):
    """
    Used by Scheduler to send notifications

    :param chat_id: chat id
    :param text: message to send
    :param job_name: job name
    :return: none
    """
    for _ in range(5):
        try:
            print('<<<', config.time_now(), job_name)
            bot.send_message(chat_id=chat_id, text=text)
            break
        except Exception:
            print('!!!Exception in send_msg!!!')
            continue


def retries(func):
    """Retry decorator"""
    # todo @retry decorator (import wraps maybe?)
    print('Retry')

    def wrapper(*args, **kwargs):
        for i in range(5):
            try:
                func(*args, **kwargs)
                break
            except Exception:
                print(f'Exception occured, {i}...')
                continue

    return wrapper()


if __name__ == '__main__':
    txt = ''


    @bot.message_handler(func=lambda x: x.text == 'jobs')
    def jobs_comm(x):
        Scheduler.print_jobs()


    @bot.message_handler(func=lambda x: handler_STATE == 'init')
    # todo Make this decorator for retries work here!!!
    # @ retry
    def message_listen(update):
        global handler_STATE
        global txt
        txt = update.text
        bot.send_message(chat_id=update.chat.id,
                         text='When to remind\n{}?'.format(txt),
                         reply_markup=markup)
        handler_STATE = 'date_listen'


    @bot.message_handler(func=lambda x: handler_STATE == 'date_listen')
    def date_listen(update):
        global txt
        global handler_STATE
        for _ in range(5):
            try:
                if date_parse(update.text) == 'FUCK!!':
                    bot.send_message(update.chat.id, 'FUCK!!!', reply_markup=ReplyKeyboardRemove())
                else:
                    time = date_parse(update.text)
                    msg = '"{}"\n is set at\n {}'.format(txt, time.strftime('%H:%M:%S %d.%m.%Y'))
                    Scheduler.add_job(time=time,
                                      text=txt,
                                      chat_id=update.chat.id,
                                      job_name='{} * {}'.format(update.chat.username,
                                                                update.text))
                    bot.send_message(update.chat.id, msg, reply_markup=ReplyKeyboardRemove())
                break
            except Exception:
                print('!!!Exception in date_listen!!!')
                continue
        txt = ''
        handler_STATE = 'init'


    print('beep')

    Scheduler.scheduler.start()
    Scheduler.print_jobs()

    for _ in range(5):
        try:
            bot.infinity_polling(True)
            # break
        except Exception:
            print('Exception in bot.infinity_polling')
            continue
