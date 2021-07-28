from discord.ext.commands import Bot, Cog, Context, command, guild_only
from discord.ext.commands.errors import MissingRequiredArgument
from helpers.basics import say


class Hello(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    @guild_only()
    async def hello(self, ctx: Context):
        """Noodle says hello!"""
        await say(ctx.channel, "Salutations")

    @command()
    @guild_only()
    async def say(self, ctx: Context, *, message: str):
        """Noodle repeats a message."""
        await ctx.message.delete()
        await say(ctx.channel, message)

    @say.error
    async def say_error(self, ctx: Context, e: Exception):
        if isinstance(e, MissingRequiredArgument):
            await say(ctx.channel, "You should tell me what to say.")


def setup(bot: Bot):
    bot.add_cog(Hello(bot))
