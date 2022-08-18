from discord.ext import commands, tasks


class Track(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}')

    @tasks.loop()  # how long?
    async def sync_database(self):
        # if eddb has new dumps, update (locking commands in the meantime) https://eddb.io/api
        # get live prices from Tromador's eddblink server http://elite.tromador.com/files/listings-live.csv
        ...

    @commands.command()
    async def trackbuy(self, ctx, commodity: str, price: int, system: str, range: int):
        ...


def setup(bot: commands.Bot):
    bot.add_cog(Track(bot))


def teardown(bot: commands.Bot):
    bot.remove_cog('Track')
