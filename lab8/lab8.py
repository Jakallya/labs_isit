# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot import apihelper
import requests

# Настройка прокси
# apihelper.proxy = {
#     'https': 'socks5h://bmstu:welcome_@94.103.82.136:1080'
# }

TOKEN = '8179088457:AAF1KMTfZM82LBaOGpGOD1d4l0WvglsHlj0'  # Замените на ваш токен
bot = telebot.TeleBot(TOKEN)

# Счётчики нажатий
counters = {
    'white_cat': 0,
    'black_cat': 0,
    'back': 0
}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Белый котик')
    btn2 = types.KeyboardButton('Чёрный котик')
    markup.add(btn1, btn2)

    bot.send_message(
        message.chat.id,
        'Привет! Выбери котика:',
        reply_markup=markup
    )

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id

    if message.text == 'Белый котик':
        counters['white_cat'] += 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Посмотреть белого котика')
        btn2 = types.KeyboardButton('Назад')
        markup.add(btn1, btn2)

        bot.send_message(
            chat_id,
            f'Белый котик выбран {counters["white_cat"]} раз(а). Что дальше?',
            reply_markup=markup
        )

    elif message.text == 'Чёрный котик':
        counters['black_cat'] += 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Посмотреть чёрного котика')
        btn2 = types.KeyboardButton('Назад')
        markup.add(btn1, btn2)

        bot.send_message(
            chat_id,
            f'Чёрный котик выбран {counters["black_cat"]} раз(а). Что дальше?',
            reply_markup=markup
        )

    elif message.text == 'Посмотреть белого котика':
        # Отправка изображения белого кота
        img_url = 'https://i.pinimg.com/474x/5b/57/d7/5b57d7a94dc0bd003e000bb7a6ff47e6.jpg'
        bot.send_photo(chat_id, img_url, caption='Вот ваш белый котик! 😊')

    elif message.text == 'Посмотреть чёрного котика':
        # Отправка изображения чёрного кота
        img_url = 'https://i.pinimg.com/474x/b2/b5/d9/b2b5d94c9aafe34de5eb4bb131bb395a.jpg'
        bot.send_photo(chat_id, img_url, caption='Вот ваш чёрный котик! 😊')

    elif message.text == 'Назад':
        counters['back'] += 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Белый котик')
        btn2 = types.KeyboardButton('Чёрный котик')
        markup.add(btn1, btn2)

        bot.send_message(
            chat_id,
            f'Вы вернулись назад. Назад нажато {counters["back"]} раз(а). Выберите котика:',
            reply_markup=markup
        )

# Запуск бота
bot.polling(none_stop=True)