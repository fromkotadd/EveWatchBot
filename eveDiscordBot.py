import asyncio
import config
import discord
from discord.ext import commands
import datetime
import os


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents) #инициализируем бота с префиксом '!'
TIMEOUT = 30
ID_CHANNEL = 1043936080224854089
@bot.command()
async def test(ctx):
	author = discord.Member.id
	await ctx.send(f'Hello, {author}!')


@bot.event
async def on_ready():
    channel = bot.get_channel(ID_CHANNEL)
    while True:
        try:
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'object_create.jpg')
            if path:
                time_now = datetime.datetime.today().strftime("%H:%M:%S")
                file = discord.File(f'C:\pythonProject\EveWatchBot\object_create.jpg', filename=f'object_create.jpg')
                emned = discord.Embed(color=0xff9900, title=f'time: {time_now}')
                emned.set_image(url=f"attachment://object_create.jpg")
                print('screen download to chanel')
                await channel.send(file=file, embed=emned)
            else:
                continue
        except (FileNotFoundError, discord.errors.HTTPException) as EX:
            print(EX)
            continue
        await asyncio.sleep(TIMEOUT)

bot.run(config.TOKEN)
