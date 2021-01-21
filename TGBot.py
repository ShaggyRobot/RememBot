import config

import telegram
from telegram.ext import Updater, MessageHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import ReplyKeyboardMarkup as ReplyKeyboard
from telegram import ReplyKeyboardRemove as RemoveKeyboard
from telegram import InlineKeyboardButton as Key

import Scheduler

from date_parse import date_parse

bot = telegram.Bot(token=config.token)
updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher
txt = ''

keypad = ([
    [Key('10min', callback_data='in 10 min'),
     Key('15min', callback_data='in 15 min'),
     Key('1hour', callback_data='in 60 min'),
     Key('Tomorrow', callback_data='tomorrow'),
     ],
    [Key('space_holder', callback_data=None)]
])

keyboard = ReplyKeyboard(keypad,
                         resize_keyboard=True,
                         one_time_keyboard=True)


def send_msg(chat_id: int, text: str):
    """
    Used by Scheduler to send notifications

    :param chat_id: chat id
    :param text: message to send
    :return: none
    """

    bot.sendMessage(chat_id=chat_id, text=text)


if __name__ == '__main__':

    def message_listen(update, context):
        global txt
        if update.message.text == 'jobs':
            Scheduler.print_jobs()
        else:
            txt = update.message.text
            bot.sendMessage(chat_id=update.message.chat.id,
                            text='When to remind\n{}?'.format(txt),
                            reply_markup=keyboard)
            dispatcher.remove_handler(msglstn)
            dispatcher.add_handler(keyboard_listen)
            dispatcher.add_handler(datelisten)


    def key_press(update, context):
        time = date_parse(update.callback_query.data)
        msg = '"{}"\n is set at\n {}'.format(txt, time.strftime('%H:%M:%S %d.%m.%Y'))
        Scheduler.add_job(time=time,
                          text=txt,
                          chat_id=update.effective_chat.id,
                          job_name='{} * {}'.format(update.effective_chat.username,
                                                    update.callback_query.data))
        bot.sendMessage(chat_id=update.effective_chat.id, text=msg)
        dispatcher.remove_handler(datelisten)
        dispatcher.remove_handler(keyboard_listen)
        dispatcher.add_handler(msglstn)


    def date_listen(update, context):
        global txt
        time = date_parse(update.message.text)
        msg = '"{}"\n is set at\n {}'.format(txt, time.strftime('%H:%M:%S %d.%m.%Y'))
        Scheduler.add_job(time=time,
                          text=txt,
                          chat_id=update.message.chat.id,
                          job_name='{} * {}'.format(update.message.chat.username,
                                                    update.message.text))
        bot.sendMessage(chat_id=update.message.chat.id, text=msg, reply_markup=RemoveKeyboard(keyboard))
        txt = ''
        # RemoveKeyboard()
        dispatcher.remove_handler(datelisten)
        dispatcher.add_handler(msglstn)


    keyboard_listen = CallbackQueryHandler(key_press)
    msglstn = MessageHandler(~Filters.command, message_listen)
    datelisten = MessageHandler(~Filters.command, date_listen)

    dispatcher.add_handler(msglstn)

    Scheduler.scheduler.start()
    Scheduler.print_jobs()
    updater.start_polling(clean=True)

    print('beep...')
