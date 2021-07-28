from discord.ext.commands import Bot, Cog, Context, command, guild_only
from helpers.basics import say
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
                message = f"{query} is even."
            else:
                message = f"{query} is not even."
        except Exception as e:
            message = str(e)
        await say(ctx.channel, message)


def setup(bot: Bot):
    bot.add_cog(Meme(bot))
