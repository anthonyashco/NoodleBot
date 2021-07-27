from discord import Color, Embed
from discord.ext.commands import Cog, command, guild_only
import re


class Hello(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command()
    @guild_only()
    async def hello(self, ctx):
        """Noodle says hello!"""
        embed = Embed(description="Sssalutationsss.", color=Color.orange())
        await ctx.channel.send(embed=embed)

    @command()
    @guild_only()
    async def say(self, ctx, *, message: str):
        """Noodle repeats a message."""
        await ctx.message.delete()
        messsage = re.sub(r"(ss|s)", "sss", message)
        messsage = re.sub(r"(Ss|S)", "Sss", messsage)
        embed = Embed(description=messsage, color=Color.orange())
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Hello(bot))
