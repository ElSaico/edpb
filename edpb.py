import logging
import os

import discord
import dotenv
from discord.ext import commands, tasks
from discord.utils import oauth_url

from db import db

PERMISSION_FLAGS = 3072

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='ed!', intents=intents)
db.connect()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Invite link: {oauth_url(bot.user.id, permissions=discord.Permissions(PERMISSION_FLAGS))}')


@tasks.loop()  # how long?
async def sync_database():
    # if eddb has new dumps, update (locking commands in the meantime) https://eddb.io/api
    # get live prices from Tromador's eddblink server http://elite.tromador.com/files/listings-live.csv
    ...


@bot.command()
async def trackbuy(ctx, commodity: str, price: int, system: str, range: int):
    ...


bot.run(os.getenv('TOKEN'))
