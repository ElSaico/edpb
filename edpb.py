import logging
import os

import dotenv
from discord.ext import commands

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='ed!')

bot.load_extension('modules.track')
bot.run(os.getenv('TOKEN'))
