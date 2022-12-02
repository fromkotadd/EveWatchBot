import asyncio
import pytesseract
from config import config
import discord
from discord.ext import commands
import datetime
import cv2
import mss
import numpy as np
import json
import re

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)  # инициализируем бота с префиксом '!'
ID_CHANNEL = config['ID_CHANNEL']

pytesseract.pytesseract.tesseract_cmd = config['PATH_PYTESSERACT']
TIMEOUTH = config['TIMEOUTH']

with open('date/mouse_poss_for_grid_parser.json') as file_0, open('date/ally_tag_white_list.json') as file_1:
    """load pars area coordinates and ally tag list"""
    parse_grid_triggerJSON = json.load(file_0)  # pars area in overview
    white_list = json.load(file_1)


def time():
    """time now"""
    return datetime.datetime.today().strftime("%H:%M:%S")


def grid_trigger(parse_area):
    """ parsing text to search for a tag"""

    img = np.asarray(mss.mss().grab(parse_area))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    pars_string = pytesseract.image_to_string(hsv)
    # print(len(pars_string))
    pattern_1 = r'[(\[{\|]'r'\w{2,4}'r'[)\]}\|]'  # for find corp tag
    if pars_string:
        for word in pars_string.replace('\n', ' ').split(' '):
            print(word)
            if re.search(pattern_1, word):
                teg = re.search(pattern_1, word).group()[1:-1]
                print(teg)
                if teg.upper() not in white_list:
                    print(f'enemy teg - {teg.upper()}')
                    return True
        if not re.search(pattern_1, pars_string):
            return True
    else:
        return False
    return False


def sentry_bot(search_technology, parse_greed_trigger, TIMEOUT=5):
    @bot.event
    async def on_ready():
        channel = bot.get_channel(ID_CHANNEL)
        while True:
            result = search_technology(parse_greed_trigger)
            if result:
                mss.mss().shot(output=f'object_create.jpg')
                file = discord.File(f'C:/PycharmProjects/EveWatchBot/object_create.jpg', filename=f'object_create.jpg')
                emned = discord.Embed(color=0xff9900, title=f'time: {time()}')
                emned.set_image(url=f"attachment://object_create.jpg")
                print('Screen download to chanel')
                await channel.send(file=file, embed=emned)
                await asyncio.sleep(TIMEOUT)

            else:
                print(f'Continue\t{time()}')
                await asyncio.sleep(1)


if __name__ == '__main__':
    sentry_bot(grid_trigger, parse_grid_triggerJSON, TIMEOUT=TIMEOUTH)
    bot.run(config['TOKEN'])
