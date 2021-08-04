from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext
from discord_slash.cog_ext import cog_slash
from helpers.basics import say


class Slash(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_slash(name="ping")
    async def ping(self, ctx: SlashContext):
        await say(ctx.channel, f"Pong! ({self.bot.latency*1000}ms)")


def setup(bot: Bot):
    bot.add_cog(Slash(bot))
