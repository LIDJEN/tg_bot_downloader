import telebot
from api import token
from logic import *

bot = telebot.TeleBot(token)

help_msg = []
help_msg.append("send me youtube link, like this:\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ")


@bot.message_handler(commands=['help', 'start'])
def send_help(message):
    bot.send_message(message.chat.id, "".join(help_msg), parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def send_text(message):
    if check_if_youtube_link(message.text):
        download_video(message.text)
    else:
        bot.send_message(message.chat.id, help_msg)

bot.polling()