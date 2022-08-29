import logging
import os

import discord
import dotenv
import playhouse.apsw_ext as pw
from discord.ext import commands
from discord.utils import oauth_url

import eddb
import models

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


# TODO enforce positive values for price, radius and quantity
@bot.command()
async def trackbuy(ctx, commodity: str, price: int, system: str, radius: int, quantity: int):
    """Create a price alert for when a commodity can be bought below a target value, given a specified radius from a
    central system and a minimum supply."""
    try:  # TODO make case-insensitive
        commodity = models.Commodity.get(models.Commodity.name == commodity)
    except pw.DoesNotExist:
        ...


@bot.command()
async def tracksell(ctx, commodity: str, price: int, system: str, radius: int, quantity: int):
    """Create a price alert for when a commodity can be sold above a target value, given a specified radius from a
    central system and a minimum demand."""
    ...


@bot.command()
async def tracklist(ctx):
    """Get a list of all your price alerts."""
    ...


@bot.command()
async def trackdel(ctx, track_id: int):
    """Remove a price alert by giving its ID number."""
    ...


bot.run(os.getenv('TOKEN'))
