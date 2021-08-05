from __main__ import settings
from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext as ctx
from discord_slash.cog_ext import cog_slash
from discord_slash.model import SlashCommandOptionType as opt
from discord_slash.utils.manage_commands import create_option
from helpers.basics import say

guild_ids = settings["slash"]["guilds"]


class Hello(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_slash(guild_ids=guild_ids)
    async def hello(self, ctx: ctx):
        """Noodle says hello!"""
        await say(ctx, "Salutations")

    @cog_slash(guild_ids=guild_ids,
               options=[
                   create_option("message", "The message to repeat", opt.STRING,
                                 True)
               ])
    async def say(self, ctx: ctx, message: str):
        """Noodle repeats a message."""
        await say(ctx, message)


def setup(bot: Bot):
    bot.add_cog(Hello(bot))
