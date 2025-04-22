import telebot
from telebot import types
import random
import json

TOKEN = '8179088457:AAF1KMTfZM82LBaOGpGOD1d4l0WvglsHlj0'
bot = telebot.TeleBot(TOKEN)

def load_cats_data():
    try:
        with open('cat_photos.json', 'r', encoding='utf-8') as file:
            cats_data = json.load(file)
            return {cat_type: {**data, 'votes': 0} for cat_type, data in cats_data.items()}
    except FileNotFoundError:
        print("Файл cats_photos.json не найден")
        return {}
    except json.JSONDecodeError:
        print("Ошибка при чтении JSON-файла")
        return {}

cats_db = load_cats_data()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🐱 Выбрать котика')
    btn2 = types.KeyboardButton('📊 Результаты голосования')
    btn3 = types.KeyboardButton('ℹ️ О проекте')
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id,
                    "Добро пожаловать в CatVoteBot!\n"
                    "Здесь вы можете голосовать за самых красивых котиков.",
                    reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id

    if message.text == '🐱 Выбрать котика':
        send_cat_selection(chat_id)
    elif message.text == '📊 Результаты голосования':
        send_vote_results(chat_id)
    elif message.text == 'ℹ️ О проекте':
        bot.send_message(chat_id,
                        "CatVoteBot - система голосования за котиков\n"
                        "Разработано для лабораторной работы по созданию inline-меню")

def send_cat_selection(chat_id):
    if not cats_db:
        bot.send_message(chat_id, "Извините, данные о котиках временно недоступны.")
        return

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = []

    for cat_type in cats_db.keys():
        btn = types.InlineKeyboardButton(
            text=f'{cat_type} ({cats_db[cat_type]["votes"]}❤️)',
            callback_data=f'cat_{cat_type}')
        buttons.append(btn)

    keyboard.add(*buttons)
    bot.send_message(chat_id,
                    "Выберите тип котика:",
                    reply_markup=keyboard)

def send_vote_results(chat_id):
    if not cats_db:
        bot.send_message(chat_id, "Извините, данные о котиках временно недоступны.")
        return

    results = ["📊 Результаты голосования:"]
    total_votes = sum(cat['votes'] for cat in cats_db.values())

    for cat_type, data in cats_db.items():
        percent = (data['votes'] / total_votes * 100) if total_votes > 0 else 0
        results.append(
            f"{cat_type}: {data['votes']} голосов ({percent:.1f}%)")

    bot.send_message(chat_id, "\n".join(results))

def send_cat_options(chat_id, cat_type):
    if cat_type not in cats_db:
        bot.send_message(chat_id, "Извините, этот тип котика не найден.")
        return

    cat_data = cats_db[cat_type]
    photo_url = random.choice(cat_data['photos'])

    keyboard = types.InlineKeyboardMarkup()
    btn_vote = types.InlineKeyboardButton(
        text=f'❤️ Проголосовать за этого котика ({cat_data["votes"]})',
        callback_data=f'vote_{cat_type}')
    btn_back = types.InlineKeyboardButton(
        text='🔙 К выбору котиков',
        callback_data='back_to_cats')
    keyboard.add(btn_vote)
    keyboard.add(btn_back)

    bot.send_photo(chat_id, photo_url,
                  caption=f"{cat_type} котик\n{cat_data['description']}",
                  reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data.startswith('cat_'):
        cat_type = call.data[4:]
        send_cat_options(chat_id, cat_type)
        bot.answer_callback_query(call.id)

    elif call.data.startswith('vote_'):
        cat_type = call.data[5:]
        if cat_type in cats_db:
            cats_db[cat_type]['votes'] += 1

            try:
                bot.answer_callback_query(
                    call.id,
                    f"Вы проголосовали за {cat_type} котика!")

                cat_data = cats_db[cat_type]
                keyboard = types.InlineKeyboardMarkup()
                btn_vote = types.InlineKeyboardButton(
                    text=f'❤️ Проголосовать за этого котика ({cat_data["votes"]})',
                    callback_data=f'vote_{cat_type}')
                btn_back = types.InlineKeyboardButton(
                    text='🔙 К выбору котиков',
                    callback_data='back_to_cats')
                keyboard.add(btn_vote)
                keyboard.add(btn_back)

                bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=keyboard)
            except Exception as e:
                print(f"Ошибка при обновлении сообщения: {e}")

    elif call.data == 'back_to_cats':
        bot.delete_message(chat_id, message_id)
        send_cat_selection(chat_id)
        bot.answer_callback_query(call.id)

if __name__ == '__main__':
    print("Бот запущен и готов показывать котиков!")
    bot.polling(none_stop=True)