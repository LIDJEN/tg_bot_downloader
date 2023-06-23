# import pytube
# from pytube import YouTube
import os
import pafy
import sqlite3
from telebot import types

#################################
## создание и подключение к бд ##
#################################
con = sqlite3.connect("YouTube_download_bot")
global db
db = con.cursor()
db.execute("CREATE TABLE IF NOT EXISTS chat_history (chat_id int, message TEXT, resolution TEXT)")


######################
## Работа с ссылкой ##
######################
def download_video(url: str, resolution: str):
    video = pafy.new(url)
    video.resolution = resolution
    video.download(output_path="./videos")
def get_video_resolutions(url):
    return ["123"]
    video = pafy.new(url)
    streams = []
    for stream in video.videostreams:
        streams.append(stream.resolution)
    return streams

# def download_video(url: str, resolution: str):
#     path = "./videos"  # Path to save the video
#     video = YouTube(url)
#     stream = video.streams.get_by_resolution(resolution)
#     if stream:
#         # await asyncio.sleep(0)  # Allow other tasks to run
#         stream.download(path)
#         return video.title
#     else:
#         return None
#
# def get_video_resolutions(url):
#     video = pytube.YouTube(url)
#     stream=[]
#     print(video.title)
#     for streams in video.streams.filter(file_extension='mp4').all():
#         stream.append(str(streams).split()[3])
#
#     # res = set(stream)
#     ret = []
#     for i in stream:
#         # if "kbps" in i:
#         #     continue
#         ret.append(i[i.index("=")+2:-1])
#     return ret
#
#

def delete_video(name):
    os.remove(name)

############################################
## История чата запись/чтение/удаление бд ##
############################################
def add_history(chat_id:int, link:str, res:str):
    db.execute("INSERT INTO chat_history (chat_id, message, resolution) VALUES (?, ?, ?)", (chat_id, link, res))

def get_history(chat_id):
    query = f"SELECT message FROM chat_history WHERE chat_id={chat_id}"
    result = db.execute(query).fetchone()
    if result:
        query = f"SELECT message FROM chat_history WHERE chat_id={chat_id}"
        history = db.execute(query).fetchall()
        return tuple(zip(*history))[0]
    else:
        return "Запросов не было"

def del_history(chat_id):
    query = f"SELECT * FROM chat_history WHERE chat_id={chat_id}"
    result = db.execute(query).fetchone()
    if result:
        db.execute(f"DELETE FROM chat_history WHERE chat_id={chat_id}")
        return "История удалена"
    else:
        return"История удалена"


############################
## Telebot reply keyboard ##
############################

def create_inline_keyboard(options):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    for resolution in options:
        markup.add(types.KeyboardButton(resolution))
    return markup

# def create_inline_markup(options):
#     keyboard = types.InlineKeyboardMarkup()
#     for option in options:
#         label = callback_data = option
#         button = types.InlineKeyboardButton(label, callback_data=callback_data)
#         keyboard.add(button)
#     return keyboard

# streams = ["176x144","640x360"]
# create_inline_keyboard(streams)