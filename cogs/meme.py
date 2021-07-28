from discord import Color, Embed
from discord.ext.commands import Bot, Cog, Context, command, guild_only
from helpers.snek import snekkify
from is_even import is_even


class Meme(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=["iseven"])
    @guild_only()
    async def is_even(self, ctx: Context, query: int):
        """Check if integer is even using isevenapi"""
        try:
            ie = is_even.is_even(int(query))
            if ie:
                description = f"{query} is even."
            else:
                description = f"{query} is not even."
        except Exception as e:
            description = str(e)
        embed = Embed(description=snekkify(description), color=Color.orange())
        await ctx.channel.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Meme(bot))
