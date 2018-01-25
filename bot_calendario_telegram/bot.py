#!/usr/bin/env python
"""Serve a bot in telegram."""

# External imports
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler)
import json
import logging

# Local improts
import context
from bot_calendario_telegram.settings import BOT_TOKEN
from bot_calendario_telegram import connect_reminder

assert context

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

# Event Creation Steps
GET_EVENT_DATE, CONFIRM, END_CREATE_CONVER = range(3)

event_info = dict()


def start(bot, update):
    update.message.reply_text('Hola! ¿Qué hay?')


def status(bot, update):
    status = connect_reminder.status()
    update.message.reply_text(status)


def list_events(bot, update):
    events = connect_reminder.list_events()
    update.message.reply_text('Los eventos guardados son: {}'.format(
        json.dumps(events, indent=2, ensure_ascii=False)))


def add_event(bot, update):
    user = update.message.from_user
    logger.info('Creating event')
    update.message.reply_text(
        'Introduzca el ID del evento a gruardar:',
        reply_markup=ReplyKeyboardRemove())

    return GET_EVENT_DATE


def get_reminder_datetime(bot, update):
    user = update.message.from_user
    event_info['event_id'] = update.message.text

    logger.info('Event ID: \'{}\' from user \'{}\''.format(
        event_info.get('event_id'), user.id))
    update.message.reply_text(
        'Introduzca la fecha del evento (con formato YYY/MM/DD HH:MM):')

    return CONFIRM


def confirm_data(bot, update):
    user = update.message.from_user
    event_info['reminder_datetime'] = update.message.text
    reply_keyboard = [['Sí', 'No']]

    logger.info('Event datetime: \'{}\' from user \'{}\''.format(
        event_info.get('reminder_datetime'), user.id))
    update.message.reply_text(
        'Los datos son los siguientes: {}\n\n¿Desea guardar los cambios?'.
        format(str(event_info)),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
    )

    return END_CREATE_CONVER


def save_event(bot, update):
    user = update.message.from_user

    output = connect_reminder.add_event(event_info)

    if output:
        # No error
        message = 'Success!'
    else:
        message = 'Oooops! Ocurrió algún error.'

    logger.info('output of save: %s', str(output))
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info('User %s canceled the conversation.', user.first_name)
    update.message.reply_text(
        'Operación cancelada.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update \'%s\' caused error \'%s\'', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_event', add_event)],
        states={
            GET_EVENT_DATE:
            [MessageHandler(Filters.text, get_reminder_datetime)],
            CONFIRM: [MessageHandler(Filters.text, confirm_data)],
            END_CREATE_CONVER: [RegexHandler('^(Sí)$', save_event)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(CommandHandler('status', status))
    dp.add_handler(CommandHandler('list_events', list_events))

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
