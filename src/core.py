"""
Basic example for a bot that uses inline keyboards.
"""
import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from src.config.settings import TELEGRAM_TOKEN
from src.cats import Cat
from src.wiki import Wiki

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Quero ver um gatinho'],
    ['Mostra um fato aleatório que o Nicolas saberia'],
    ['To bem por hora. Mais tarde a gente conversa'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update, context):
    update.message.reply_text(
        "Oiê mozão!\nEssa é a minha versão digital boladona pra você.\nEu tenho vários "
        "poderes que o Nicolas real não tem... Ser um robozinho têm suas vantagens afinal.\n"
        "O que você quer fazer? (^・ｪ・^)",
        reply_markup=markup,
    )

    return CHOOSING


def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    print(context.user_data['choice'])
    if context.user_data['choice'] == "Quero ver um gatinho":
        cat = Cat()
        try:
            url = cat.get_random_url()
            logger.info(f"sending picture from URL: {url}")
            update.message.bot.send_photo(update.message.chat_id, url, "Um gatinho saindo do forno pra ti.")
        except Exception as e:
            logger.error(e)
            update.message.reply_text(
               "aconteceu alguma coisa inesperada procurando seu gatinho dessa vez... Mas você pode tentar "
               "novamente mais tarde :)\nPosso fazer algo mais por você?", reply_markup=markup,
            )
            return CHOOSING
    elif context.user_data["choice"] == "Mostra um fato aleatório que o Nicolas saberia":
        print("got here")
        wiki = Wiki()
        try:
            data = wiki.get_random_page_info()
            logger.info(f"sending data from URL: {data['url']}")
            update.message.reply_text(f"mor!\nTe contar uma esquema sobre {data['title']}!\n"
                                      f"Cê sabia que {data['extract']}?")
        except Exception as e:
            logger.error(e)
            update.message.reply_text(
                "me perdi procurando seu fato aleatório... Mas você pode tentar "
                "novamente mais tarde :)\nPosso fazer algo mais por você?",
                reply_markup=markup,
            )
            return CHOOSING
    update.message.reply_text(
        "Espero que tenha feito seu dia um pouco mais feliz, mozão!\n"
        "Posso fazer algo mais por você?",
        reply_markup=markup,
    )
    return CHOOSING


def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']
    update.message.reply_text(
        "Tranquilo mozão. Volta logo, viu =^._.^= ∫"
    )
    user_data.clear()

    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Quero ver um gatinho|Mostra um fato aleatório que o Nicolas saberia)$'),
                    regular_choice
                ),
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^To bem por hora. Mais tarde a gente conversa$'), done)],
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
