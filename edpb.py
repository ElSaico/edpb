import logging
import os

import discord
import dotenv
from discord.ext import commands
from discord.utils import oauth_url

import eddb
from models import db

PERMISSION_FLAGS = 3072

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='ed!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Invite link: {oauth_url(bot.user.id, permissions=discord.Permissions(PERMISSION_FLAGS))}')
    eddb.sync_database.start()


@bot.command()
async def trackbuy(ctx, commodity: str, price: int, system: str, range: int):
    ...


bot.run(os.getenv('TOKEN'))
