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
    text = message.text
    if check_if_youtube_link(text):
        reply = create_inline_keyboard()
        bot.reply_to(message, "Choose the video quality:", reply_markup=reply)
        bot.register_next_step_handler(message, download_video)
    else:
        bot.send_message(message.chat.id, help_msg)

bot.polling()