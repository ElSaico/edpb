from discord.ext import commands


class Track(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}')


def setup(bot: commands.Bot):
    bot.add_cog(Track(bot))


def teardown(bot: commands.Bot):
    bot.remove_cog('Track')
