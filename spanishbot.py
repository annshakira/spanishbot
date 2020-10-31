#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the function to translate a string or list of strings
def translate(message):
    if type(message) == str:
        message = message.split()
    translation = []
    cnt = 0
    max = len(message)
    while len(message) !=0 and cnt < max:
        word = message[cnt]
        satzzeichen = False;
        ucar = ord(word[-1])
        if (ucar < ord('A') or ucar > ord('Z')) and (ucar < ord('a') or ucar > ord('z')):
             satzzeichen = True
             symbol = word [-1]
             word = word[:-1]
        if len(word) != 0 and (word[-1] == 'e' or word[-1] == 'o'):
            word = word[:-1]
        if len(message) == 1:
            if ord(word[0]) > ord('A') and ord(word[0]) < ord('Z'):
                word = chr(ord(word[0]) + (ord('a') - ord('A'))) + word[1:]
            word = "Mucho " + word
            word += 'o'
        else:
            word += "os"
        if cnt % 3 == 1:
            word = "muchos " + word
        if satzzeichen:
            word += symbol
        translation.append(word)
        cnt += 1
    return translation

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hello there. I'm a universal translator who will translate any phrase from any language to spanish. Try me out here or use me directly in your conversation.")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def print_translation(update, context):
    message = update.message.text
    translation = translate(message)
    update.message.reply_text(' '.join(translation))

def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Translation",
            input_message_content=InputTextMessageContent(translate(query)))]

    update.inline_query.answer(results)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1028875723:AAHY6e6ZHbM8k2AjfQVWFfJ8wxe3TlQ_2eY", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, print_translation))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
