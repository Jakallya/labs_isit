from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import xml.dom.minidom
import requests

TOKEN = "8179088457:AAF1KMTfZM82LBaOGpGOD1d4l0WvglsH***"
DEFAULT_CURRENCY = "USD"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["USD", "CNY"],
        ["Ввести дату"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Привет! Я бот для получения курсов валют ЦБ РФ.\n"
        "Выбери валюту или нажми 'Ввести дату':",
        reply_markup=reply_markup
    )


async def get_currency_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text

    if user_input in ["USD", "CNY"]:
        context.user_data['currency'] = user_input
        await update.message.reply_text(f"Выбрана валюта: {user_input}. Введите дату в формате ДД.ММ.ГГГГ")
        return
    elif user_input == "Ввести дату":
        await update.message.reply_text("Введите дату в формате ДД.ММ.ГГГГ")
        return

    if "." in user_input:
        try:
            day, month, year = user_input.split(".")
            if len(day) != 2 or len(month) != 2 or len(year) != 4:
                raise ValueError
            currency = context.user_data.get('currency', DEFAULT_CURRENCY)
            rate = await fetch_currency_rate(currency, user_input)
            await update.message.reply_text(f"Курс {currency} на {user_input}: {rate:.2f} руб.")
        except ValueError:
            await update.message.reply_text("Неверный формат даты. Используйте ДД.ММ.ГГГГ")
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {str(e)}")
    else:
        await update.message.reply_text("Пожалуйста, выберите валюту или введите дату")


async def fetch_currency_rate(currency_code: str, date: str) -> float:
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    response = requests.get(url)
    response.raise_for_status()

    dom = xml.dom.minidom.parseString(response.text)
    dom.normalize()

    valutes = dom.getElementsByTagName("Valute")

    for valute in valutes:
        char_code = valute.getElementsByTagName("CharCode")[0]
        if char_code.childNodes[0].nodeValue == currency_code:
            value = valute.getElementsByTagName("Value")[0]
            rate = float(value.childNodes[0].nodeValue.replace(",", "."))
            nominal = valute.getElementsByTagName("Nominal")[0]
            nominal_value = int(nominal.childNodes[0].nodeValue)
            return rate / nominal_value

    raise ValueError(f"Валюта {currency_code} не найдена")


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_currency_rate))

    application.run_polling()


if __name__ == '__main__':
    main()