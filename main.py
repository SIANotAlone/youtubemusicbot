from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config

import youtube_dl

bot = Bot(token=config.token)
dp = Dispatcher(bot)



import sqlite3

def savetodb(chat_id, link):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    # sql.execute("""CREATE TABLE IF NOT EXISTS users (
    # user_id TEXT,
    # link TEXT
    # )""")
    # db.commit()


    # test_id = input("Enter user id for put them in database: ")
    # test_link = input('Enter link for put them in database: ')


    #sql.execute(f"INSERT INTO users VALUES ('{test_id}, {test_link}')")
    sql.execute(f"INSERT INTO log(chat_id, link) VALUES (?,?)",(chat_id,link))

    db.commit()

    # for value in sql.execute("SELECT * FROM log"):
    #     print (value)



import os, fnmatch
def findallmp3(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(name))
    return result


def findourmp3(video_id):
    current_folder = os.getcwd()
    songs = findallmp3('*.mp3', current_folder)
    i = 0

    elements = len(songs)
    # print("Кол-во элементов списка: " + str(elements))
    while i < elements:
        index = songs[i].find(video_id)

        if index < 0:
            pass
        #print (songs[i] + ' Не найдено'  + 'index = ' + str(index))
        else:

            return songs[i]
        # print (songs[i]+ ' Найдено '+ 'index = ' + str(index))

        i += 1
# def getmp3name():
#     import glob, os
#     current_folder = os.getcwd()
#     os.chdir(current_folder)
#     for file in glob.glob("*.mp3"):
#         print(file)
#         return file
def download_mp3(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except:
        pass


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    hello = "Привет юзер.🤗 \n Этот бот предназначем для загрузки музыки из Youtube. \nОтправьте боту ссылку на ютуб ролик и через несколько секунд бот вернет вам mp3 файл с вашей песней.😎"
    hello2 = '\nБот полностью бесплатный и его единственным ограничением. является размер выходного файла не больше 50мб, чего более чем достаточно для любой песни стандартной длительности.😌'
    await message.reply(hello + hello2)


@dp.message_handler()
async def echo_message(msg: types.Message):
    try:
        await bot.send_message(msg.from_user.id, "Подождите, пока бот скачает песню с ютуба, после этого он пришлет ее вам.")
        download_link = msg.text
        index = download_link.find("&")
        if index >= 0:
            get_link = download_link.split("&")
            download_mp3(get_link[0])
            index2 = get_link[0].split("=")
            video_id = index2[1]
            #print(video_id)
        else:
            download_mp3(download_link)

            if msg.text.find("list")>0:
                index2 = download_link[0].split("=")
                video_id = index2[1]
                #print('video id: ' + video_id + "\ndownload link: " + download_link[0])
                #print(video_id)
            elif msg.text.find('watch?v=')>0:
                index2 = msg.text.split('=')
                video_id = index2[1]
                #print('video id: ' + video_id+"\ndownload link: " + download_link[0])
            elif msg.text.find('youtu.be')>0:
                index2 = download_link.split("/")
                video_id = index2[3]

                #print(video_id)

        #song = getmp3name()

        oursong = findourmp3(video_id)

        await bot.send_audio(msg.from_user.id, open(oursong, 'rb'), "Вот ваша песня 😊")
        #print("Кол-во песен в плейлисте: " + str(len(song))  +  "    " + str(song))
        os.remove(oursong)
        savetodb(msg.from_user.id, msg.text)
    except:
        await bot.send_message(msg.from_user.id, "Что пошло не так 😭\nВозможно вы указали неверную ссылку либо объем файла превышает 50 мегабайт.\nПопробуйте еще раз.")





if __name__ == '__main__':
    executor.start_polling(dp)