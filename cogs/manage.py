"""Bot management functions for the bot owner."""

from discord.ext.commands import Bot, Cog, Context, command, group, guild_only, is_owner
from helpers.basics import say
import os
import subprocess


class Manage(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @group(aliases=["git"])
    @guild_only()
    @is_owner()
    async def manage(self, ctx: Context):
        """The main manage group. git is an alias purely for typing git pull."""
        if ctx.invoked_subcommand is None:
            await say(ctx.channel, "Forgot how to use it?")

    @manage.command()
    async def pull(self, ctx: Context):
        """Performs git pull in the terminal."""
        try:
            if ".git" in os.listdir():
                p = subprocess.run("git pull",
                                   capture_output=True,
                                   check=True,
                                   shell=True,
                                   text=True)
                await say(ctx.channel, p.stdout)
        except subprocess.CalledProcessError:
            await say(ctx.channel, "This ain't it, chief.")

    @manage.command()
    async def reload(self, ctx: Context, cog: str = None):
        """Reloads a cog after pulling updates.

        Args:
            cog (str, optional): The cog to reload. Defaults to None.
        """
        if cog is not None:
            try:
                self.bot.reload_extension("cogs." + cog)
                await say(ctx.channel, f"The {cog} cog was reloaded.")
            except Exception as e:
                print(e)
                await say(ctx.channel, "Something went wrong...")

    @manage.command()
    async def load(self, ctx: Context, cog: str = None):
        """Load a new cog.

        Args:
            cog (str, optional): The cog to load. Defaults to None.
        """
        if cog is not None:
            try:
                self.bot.load_extension("cogs." + cog)
                await say(ctx.channel, f"The {cog} cog was loaded.")
            except Exception as e:
                print(e)
                await say(ctx.channel, "Something went wrong...")

    @manage.command()
    async def unload(self, ctx: Context, cog: str = None):
        """Unload an existing cog.

        Args:
            cog (str, optional): The cog to unload. Defaults to None.
        """
        if cog is not None:
            try:
                self.bot.unload_extension("cogs." + cog)
                await say(ctx.channel, f"Alright, the {cog} cog was unloaded.")
            except Exception as e:
                print(e)
                await say(ctx.channel, "Something went wrong...")

    @command()
    @guild_only()
    @is_owner()
    async def exit(self, ctx: Context):
        """Take a break and shut down."""
        await say(ctx.channel, "Sure, I'll see you later.")
        await self.bot.close()
        print("Client closed.")


def setup(bot: Bot):
    bot.add_cog(Manage(bot))
