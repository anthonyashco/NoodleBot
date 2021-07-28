from discord import Color, Embed
from discord.ext.commands import Bot, Cog, Context, command, guild_only
from discord.ext.commands.errors import MissingRequiredArgument
from helpers.snek import snekkify


class Hello(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    @guild_only()
    async def hello(self, ctx: Context):
        """Noodle says hello!"""
        embed = Embed(description=snekkify("Salutations"), color=Color.orange())
        await ctx.channel.send(embed=embed)

    @command()
    @guild_only()
    async def say(self, ctx: Context, *, message: str):
        """Noodle repeats a message."""
        await ctx.message.delete()
        embed = Embed(description=snekkify(message), color=Color.orange())
        await ctx.channel.send(embed=embed)

    @say.error
    async def say_error(self, ctx: Context, e: Exception):
        if isinstance(e, MissingRequiredArgument):
            await ctx.channel.send()


def setup(bot: Bot):
    bot.add_cog(Hello(bot))
