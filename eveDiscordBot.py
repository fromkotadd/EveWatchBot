from config import TOKEN
import discord
import asyncio
import asyncpraw
import os

bot = discord.Client(intents=discord.Intents.default())
ID_CHANNEL = 975788405004832771



channel = bot.get_channel(975788405004832771)

# channel.send(discord.Object(id='975788405004832771'), 'hello')
channel.send(TOKEN)


bot.run(token=TOKEN)