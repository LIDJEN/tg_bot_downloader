import os
import asyncio
import pytube
from pytube import YouTube
import sqlite3
from telebot import types

#################################
## создание и подключение к бд ##
#################################
con = sqlite3.connect("YouTube_download_bot")
global db
db = con.cursor()
db.execute("CREATE TABLE IF NOT EXISTS chat_history (chat_id int, message TEXT)")


######################
## Работа с ссылкой ##
######################
async def download_video(url: str, resolution: str):
    path = "./videos"  # Path to save the video
    video = YouTube(url)
    stream = video.streams.get_by_resolution(resolution)
    if stream:
        # await asyncio.sleep(0)  # Allow other tasks to run
        stream.download(path)
        return video.title
    else:
        return None

def video_resolutions(url):
    video = pytube.YouTube(url)
    stream=[]
    for streams in video.streams:
        stream.append(str(streams).split()[3])
    return stream


def check_if_youtube_link(url):
    if "https://youtu.be/" in url \
            or "https://www.youtube.com/watch?v=" in url:
        return True
    else:
        return False

def delete_video(name):
    os.remove(name)


############################################
## История чата запись/чтение/удаление бд ##
############################################
def add_history(chat_id:int, link:str):
    db.execute("INSERT INTO chat_history (chat_id, message) VALUES (?, ?)", (chat_id, link))

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
    keyboard = types.InlineKeyboardMarkup()
    for option in options:
        label, callback_data = option
        button = types.InlineKeyboardButton(label, callback_data=callback_data)
        keyboard.add(button)
    return keyboard

print(video_resolutions("https://youtu.be/o17SXMKG7LU"))

loop = asyncio.get_event_loop()
loop.run_until_complete(download_video("https://youtu.be/o17SXMKG7LU", "480p"))

