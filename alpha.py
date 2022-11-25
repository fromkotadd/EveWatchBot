import asyncio

import pytesseract

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
ID_CHANNEL = 1045631088577486898

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

with open('mouse_poss\mause_poss_for_local_parser.json') as file_0, open('mouse_poss\mause_poss_for_greed_parser.json') as file_1:
    """load pars area coordinates"""
    parse_area_color_triggerJSON = json.load(file_0)
    parse_greed_triggerJSON = json.load(file_1)



def time():
    return datetime.datetime.today().strftime("%H:%M:%S")


def color_trigger(parse_area):
    img = np.asarray(mss.mss().grab(parse_area))
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

        if 700 > area > 500:
            return True
        else:
            pass

    return False

def greed_trigger(parse_area):

    img = np.asarray(mss.mss().grab(parse_area))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    pars_string = pytesseract.image_to_string(hsv)
    if pars_string:
        print(pars_string)
        return pars_string
    else:
        return False


def sentry_bot(search_technology, parse_greed_trigger, TIMEOUT=5):
    @bot.event
    async def on_ready():
        channel = bot.get_channel(ID_CHANNEL)
        # control = ''
        while True:
            if search_technology(parse_greed_trigger):
                mss.mss().shot(output=f'object_create.jpg')
                file = discord.File(f'C:\PycharmProjects\EveWatchBot\object_create.jpg', filename=f'object_create.jpg')
                emned = discord.Embed(color=0xff9900, title=f'time: {time()}')
                emned.set_image(url=f"attachment://object_create.jpg")
                print('Screen download to chanel')
                await channel.send(file=file, embed=emned)
                await asyncio.sleep(TIMEOUT)

            else:
                print(f'Continue\t{time()}')
                await asyncio.sleep(1)





if __name__ == '__main__':
    # sentry_bot(color_trigger, parse_area_color_triggerJSON, TIMEOUT=10)
    sentry_bot(greed_trigger, parse_greed_triggerJSON, TIMEOUT=10)
    bot.run(config.TOKEN)
