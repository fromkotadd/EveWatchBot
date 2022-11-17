import asyncio

import config
import discord
from discord.ext import commands
import datetime
import cv2
import mss
import numpy as np
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents) #инициализируем бота с префиксом '!'
TIMEOUT = 10
ID_CHANNEL = 975788405004832770

with open('mouse_poss\mouse_poss.json') as file:
    parse_area = json.load(file)
def cv2ParseModule(parse_area):
    sct = mss.mss()

    # while True:

    img = np.asarray(sct.grab(parse_area))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 50, 50])  # диапазон цвета HSV
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask0 + mask1

    contours0, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # перебираем все найденные контуры в цикле
    for cnt in contours0:
        rect = cv2.minAreaRect(cnt)  # пытаемся вписать прямоугольник
        area = int(rect[1][0] * rect[1][1])  # вычисление площади

        if area > 500:
            print(area)
            print("ENEMY IN THE HOME")
            return True
        else:
            print("RED NOT detected!")
            print("New search...")
    print('False -------')
    return False


@bot.event
async def on_ready():
    channel = bot.get_channel(ID_CHANNEL)

    while True:
        if  cv2ParseModule(parse_area):
            time_now = datetime.datetime.today().strftime("%H:%M:%S")
            mss.mss().shot(output=f'object_create.jpg')
            file = discord.File(f'C:\pythonProject\EveWatchBot\object_create.jpg', filename=f'object_create.jpg')
            emned = discord.Embed(color=0xff9900, title=f'time: {time_now}')
            emned.set_image(url=f"attachment://object_create.jpg")
            print('screen download to chanel')
            await channel.send(file=file, embed=emned)
            await asyncio.sleep(TIMEOUT)

        else:
            print('continue')
            await asyncio.sleep(TIMEOUT)
            continue

bot.run(config.TOKEN)




