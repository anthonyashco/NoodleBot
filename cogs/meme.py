from discord.ext.commands import Bot, Cog, Context, command, guild_only
from helpers.basics import say
import requests


class Meme(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=["iseven"])
    @guild_only()
    async def is_even(self, ctx: Context, query: int):
        """Check if integer is even using isevenapi"""
        try:
            r = requests.get(
                url=f"https://api.isevenapi.xyz/api/iseven/{query}/")
            ie = r.json()
            if ie["iseven"]:
                message = f"{query} is even.\n\n{ie['ad']}"
            else:
                message = f"{query} is not even.\n\n{ie['ad']}"
        except KeyError:
            message = ie["error"]
        except Exception as e:
            message = str(e)
        await say(ctx.channel, message)


def setup(bot: Bot):
    bot.add_cog(Meme(bot))
