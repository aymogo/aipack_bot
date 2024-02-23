import logging

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

TOKEN = "6585019453:AAHvf-w5wEgkaXbfPPjIa83z1KPmWK_G54Y"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

START, COMPANY_NAME, CLAIM, PHONE_NUMBER, END = range(5)

reply_keyboard = [[KeyboardButton(text='TELEFON NOMERDI JIBERIW', request_contact=True)]]

markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)



def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Assalawma aleykum\n\nKompaniyanindin atin jazip qaldirin",
    )

    return COMPANY_NAME


def company_name(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['company_name'] = text
    print(text)
    update.message.reply_text(f'Kompaniyaninz ati: {text}?\n\nMuraajatinizdi jazip qaldirin')

    return CLAIM


def claim(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['claim'] = text
    print(text)
    update.message.reply_text(f'Murajaatiniz: {text}?\n\nNomeriniz', reply_markup=markup)

    return PHONE_NUMBER


def phone_number(update: Update, context: CallbackContext) -> int:
    text = update.message.contact.phone_number
    print(type(text), text)
    context.user_data['phone_number'] = text
    update.message.reply_text(f'Muraajatiniz tez arada korip shigiladi')

    return END



def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [
                MessageHandler(
                    Filters.text, start
                ),
            ],
            COMPANY_NAME: [
                MessageHandler(
                    Filters.text, company_name
                )
            ],
            CLAIM: [
                MessageHandler(
                    Filters.text, claim
                )
            ],
            PHONE_NUMBER: [
                MessageHandler(
                    Filters.contact, phone_number
                )
            ],
            END: [
                MessageHandler(
                    Filters.text, start
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.text, start)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()