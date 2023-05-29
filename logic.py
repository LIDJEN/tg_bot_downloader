from pytube import YouTube
import sqlite3


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
def download_video(url: str, resolution="High"): # добавить асинхронность
    path = f".\\videos" # путь для скачивания видео
    video = YouTube(url)
    if resolution == "High":
        dow_vid = video.streams.get_highest_resolution()
    elif resolution == "Low":
        dow_vid = video.streams.get_lowest_resolution()
    dow_vid.download(path)
    return video.title


def check_if_youtube_link(url):
    if "https://youtu.be/" in url \
            or "https://www.youtube.com/watch?v=" in url:
        return True
    else:
        return False

def delete_video():
    pass


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


# download_video("https://youtu.be/o17SXMKG7LU")
