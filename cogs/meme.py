from discord import Color, Embed
from discord.ext.commands import Cog, command, guild_only
from is_even import is_even
import re


class Meme(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["iseven"])
    @guild_only()
    async def is_even(self, ctx, query: int):
        """Check if integer is even using isevenapi"""
        try:
            ie = is_even.is_even(int(query))
            if ie:
                description = f"{query} isss even."
            else:
                description = f"{query} isss not even."
        except Exception as e:
            message = re.sub(r"(ss|s)", "sss", str(e))
            messsage = re.sub(r"(Ss|S)", "Sss", message)
            description = messsage
        embed = Embed(description=description, color=Color.orange())
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Meme(bot))
