import logging
import requests

from telegram import (
    ReplyKeyboardMarkup,
    Update,
    ReplyKeyboardRemove,
    KeyboardButton,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# aipack
# TOKEN = "6585019453:AAHvf-w5wEgkaXbfPPjIa83z1KPmWK_G54Y"
# newew
TOKEN = "5920446143:AAE4pV6XS738rYAmTMH4zoVZdMVfdKd0B04"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

START, SELECT_LANG, COMPANY_NAME, CLAIM, PHONE_NUMBER, END = range(6)

lang_reply_keyboard = [
    [KeyboardButton(text="O'zbek tili")],
    [KeyboardButton(text="Каракалпак тили")],
    [KeyboardButton(text="Русский язык")],
]

lang_markup = ReplyKeyboardMarkup(
    lang_reply_keyboard, resize_keyboard=True, one_time_keyboard=True
)

reply_keyboard = [
    [KeyboardButton(text="TELEFON NOMERDI JIBERIW", request_contact=True)]
]

markup = ReplyKeyboardMarkup(
    reply_keyboard, resize_keyboard=True, one_time_keyboard=True
)


# Компаниянгиз номини юборинг
def start(update: Update, context: CallbackContext) -> int:
    try:
        if context.user_data["lang_code"]:
            print("COMPANY_NAME")
            lang = context.user_data["lang_code"]
            if lang == "ru":
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Здравстуйте, добро пожаловать.",
                )
                update.message.reply_text(
                    "Пожалуйста напишите название вашей компании или бренда"
                )
            if lang == "uz":
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Xush kelibsiz."
                )
                update.message.reply_text(
                    "Kompaniyangiz yoki brendingiz nomini yozing"
                )
            if lang == "qq":
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Xosh kelipsiz."
                )
                update.message.reply_text(
                    "Kompaniyańız yamasa brendingiz atınıń jazıń"
                )

            return COMPANY_NAME
    except:
        print("SELECT_LANG")
        update.message.reply_text(
            "\
            Здравстуйте, выберите язык\
            \nXush kelibsiz tilni tanlang\
            \nXosh kelipsiz tildi saylań\
            ",
            reply_markup=lang_markup,
        )
        return SELECT_LANG


def select_lang(update: Update, context: CallbackContext) -> int:
    text = update.message.text

    if text == "O'zbek tili":
        context.user_data["lang_code"] = "uz"
    elif text == "Каракалпак тили":
        context.user_data["lang_code"] = "qq"
    elif text == "Русский язык":
        context.user_data["lang_code"] = "ru"
    else:
        update.message.reply_text("Выберите язык", reply_markup=lang_markup)
        return SELECT_LANG

    lang = context.user_data["lang_code"]

    if lang == "ru":
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Русский язык выбрано.",
        )
        update.message.reply_text(
            "Пожалуйста напишите название вашей компании или бренда",
            reply_markup=ReplyKeyboardRemove(),
        )
    if lang == "uz":
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="O'zbek tili tanlandi"
        )
        update.message.reply_text(
            "Kompaniyangiz yoki brendingiz nomini yozing",
            reply_markup=ReplyKeyboardRemove(),
        )
    if lang == "qq":
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Каракалпак тили сайланды"
        )
        update.message.reply_text(
            "Kompaniyańız yamasa brendingiz atınıń jazıń",
            reply_markup=ReplyKeyboardRemove(),
        )

    # context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text="Каракалпак тили сайланды",
    # )
    # print(text)
    # update.message.reply_text(
    #     "Kompaniyanindin atin jazip qaldirin",
    #     reply_markup=ReplyKeyboardRemove(),
    # )

    return COMPANY_NAME


def company_name(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    lang = context.user_data["lang_code"]
    context.user_data["company_name"] = text
    print(text)
    # update.message.reply_text(
    #     f"Kompaniyaninz ati: {text}?\n\nMuraajatinizdi jazip qaldirin"
    # )
    if lang == "ru":
        update.message.reply_text(
            "Какие у вас проблемы возникли в связи с нашим товаром или услугой напишите подробнее."
        )
    if lang == "uz":
        update.message.reply_text(
            "Mahsulot yoki xizmatimiz bilan bog'liq qanday muammolaringiz bor? Batafsil yozing."
        )
    if lang == "qq":
        update.message.reply_text(
            "Ónim yamasa xızmetimiz menen baylanıslı qanday mashqala payda boldi? Tolıq jazıń."
        )

    return CLAIM


def claim(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    lang = context.user_data["lang_code"]
    context.user_data["claim"] = text
    print(text)
    # update.message.reply_text(
    #     f"Murajaatiniz: {text}?\n\nNomeriniz", reply_markup=markup
    # )
    if lang == "ru":
        update.message.reply_text(
            "Напишите свой телефонный номер чтобы мы могли связаться с вами.",
            reply_markup=markup,
        )
    if lang == "uz":
        update.message.reply_text(
            "Siz bilan bog'lanishimiz uchun telefon raqamingizni yozing.",
            reply_markup=markup,
        )
    if lang == "qq":
        update.message.reply_text(
            "Siz benen baylanısıwımız ushın telefon nomerińizdi jazıń.",
            reply_markup=markup,
        )

    return PHONE_NUMBER


def phone_number(update: Update, context: CallbackContext) -> int:
    text = update.message.contact.phone_number
    lang = context.user_data["lang_code"]
    print(type(text), text)
    context.user_data["phone_number"] = text
    # update.message.reply_text(
    #     f"Muraajatiniz tez arada korip shigiladi",
    #     reply_markup=ReplyKeyboardRemove(),
    # )
    if lang == "ru":
        update.message.reply_text(
            "Ваша заявка принята, мы рассмотрим вашу заявку и совсем скоро с вами свяжется менеджер Aipack!"
        )
    if lang == "uz":
        update.message.reply_text(
            "Sizning arizangiz qabul qilindi, biz sizning arizangizni ko'rib chiqamiz va Aipack menejeri tez orada siz bilan bog'lanadi!"
        )
    if lang == "qq":
        update.message.reply_text(
            "Sizdiń arzańız qabıllandı, biz sizdiń arzańızdı kórip shıǵamız hám Aipack menejeri tez arada siz benen baylanısadı!"
        )

    return END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [
                MessageHandler(Filters.text, start),
            ],
            SELECT_LANG: [MessageHandler(Filters.text, select_lang)],
            COMPANY_NAME: [MessageHandler(Filters.text, company_name)],
            CLAIM: [MessageHandler(Filters.text, claim)],
            PHONE_NUMBER: [MessageHandler(Filters.contact, phone_number)],
            END: [MessageHandler(Filters.text, start)],
        },
        fallbacks=[MessageHandler(Filters.text, start)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
