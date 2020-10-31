import telegram
bot = telegram.Bot(token='1028875723:AAHY6e6ZHbM8k2AjfQVWFfJ8wxe3TlQ_2eY')

from telegram.ext import Updaterupdater = Updater(token='1028875723:AAHY6e6ZHbM8k2AjfQVWFfJ8wxe3TlQ_2eY', use_context=True)
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message°s)', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello there. I'm a universal translator who will translate any phrase from any language to Spanish. Try me out here or use me directly in a conversation!")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
