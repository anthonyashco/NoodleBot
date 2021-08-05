from __main__ import settings
from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext as ctx
from discord_slash.cog_ext import cog_slash
from helpers.basics import say

guild_ids = settings["slash"]["guilds"]


class Slash(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_slash(guild_ids=guild_ids)
    async def ping(self, ctx: ctx):
        """Check Noodle's latency."""
        await say(ctx, f"Pong! ({self.bot.latency*1000}ms)", hidden=True)


def setup(bot: Bot):
    bot.add_cog(Slash(bot))
