import telebot
import os
import re
from logic import *
from api import token

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Что ты умеешь?")
    # btn2 = types.KeyboardButton("Прислать ссылку на ютуб")
    markup.add(btn1, )
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}, ты можешь прислать мне ссылку на видео в ютубе, которое хочешь скачать - Вот пример :send me youtube link, like this:\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ!".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(func=lambda message: re.match(r'https?://(www\.)?youtube\.com/|https?://youtu\.be/', message.text))  # youtube video download
def youtubelink(message):
    markup = create_inline_keyboard(get_video_resolutions(message.text))
    if type(markup) is str:
        bot.send_message(message.chat.id, markup)
    else:
        res = bot.reply_to(message,'choose resolution', reply_markup=markup)
        bot.register_next_step_handler(res, lambda msg: bot_video(message.chat.id, message.text, msg.text), reply_markup=menu())


    # add to DB


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Что ты умеешь?"):
        bot.send_message(message.chat.id, text="Привет, {0.first_name}, ты можешь прислать мне ссылку на видео в ютубе, которое хочешь скачать - Вот пример :send me youtube link, like this:\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ!".format(message.from_user))
#    elif check_if_youtube_link(message):

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)


    elif (message.text == "Вернуться в главное меню"):
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=menu())


    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован.")



bot.polling()