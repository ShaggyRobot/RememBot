import config
import Scheduler
from date_parse import date_parse

import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove as keyboard_remove

bot = telebot.TeleBot(config.token, parse_mode=None)

markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
buttons = (types.KeyboardButton('10m'),
           types.KeyboardButton('15m'),
           types.KeyboardButton('60m'),
           types.KeyboardButton('Tomorrow'))
markup.add(*buttons)


def send_msg(chat_id: int, text: str):
    """
    Used by Scheduler to send notifications

    :param chat_id: chat id
    :param text: message to send
    :return: none
    """

    bot.send_message(chat_id=chat_id, text=text)


if __name__ == '__main__':
    trigger = 'init'
    txt = ''


    @bot.message_handler(func=lambda x: x.text == 'jobs')
    def jobs_comm(x):
        Scheduler.print_jobs()


    @bot.message_handler(func=lambda x: trigger == 'init')
    def message_listen(update):
        global trigger
        global txt
        txt = update.text
        bot.send_message(chat_id=update.chat.id,
                         text='When to remind\n{}?'.format(txt),
                         reply_markup=markup)
        trigger = 'date_listen'


    @bot.message_handler(func=lambda x: trigger == 'date_listen')
    def date_listen(update):
        global txt
        global trigger
        if date_parse(update.text) == 'FUCK!!':
            bot.send_message(update.chat.id, 'FUCK!!!', reply_markup=keyboard_remove())
        else:
            time = date_parse(update.text)
            msg = '"{}"\n is set at\n {}'.format(txt, time.strftime('%H:%M:%S %d.%m.%Y'))
            Scheduler.add_job(time=time,
                              text=txt,
                              chat_id=update.chat.id,
                              job_name='{} * {}'.format(update.chat.username,
                                                        update.text))
            bot.send_message(update.chat.id, msg, reply_markup=keyboard_remove())
        txt = ''
        trigger = 'init'


    print('beep')

    Scheduler.scheduler.start()
    Scheduler.print_jobs()

    bot.polling()
