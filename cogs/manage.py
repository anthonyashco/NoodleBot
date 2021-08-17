"""Bot management functions for the bot owner."""

from __main__ import settings
from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext as ctx
from discord_slash.cog_ext import cog_subcommand
from discord_slash.model import SlashCommandPermissionType as perm
from discord_slash.model import SlashCommandOptionType as opt
from discord_slash.utils.manage_commands import create_option, create_permission
from helpers.basics import say
import os
import subprocess

guild_ids = settings["slash"]["guilds"]
owners = settings["owners"]
base_permissions = {}

for guild in guild_ids:
    base_permissions[guild] = []
    base_permissions[guild].append(create_permission(guild, perm.ROLE, False))
    for owner in owners:
        base_permissions[guild].append(create_permission(
            owner, perm.USER, True))


class Manage(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_subcommand(base="manage",
                    base_desc="Bot management group.",
                    base_default_permission=False,
                    base_permissions=base_permissions,
                    guild_ids=guild_ids)
    async def pull(self, ctx: ctx):
        """Performs git pull in the terminal."""
        await ctx.defer()
        try:
            if ".git" in os.listdir():
                p = subprocess.run("git pull",
                                   capture_output=True,
                                   check=True,
                                   shell=True,
                                   text=True)
                await say(ctx, p.stdout)
        except subprocess.CalledProcessError:
            await say(ctx, "This ain't it, chief.")

    @cog_subcommand(
        base="manage",
        description="Reloads a cog after pulling updates.",
        guild_ids=guild_ids,
        options=[create_option("cog", "The cog to update", opt.STRING, True)])
    async def reload(self, ctx: ctx, cog: str):
        """Reloads a cog after pulling updates.

        Args:
            cog (str, optional): The cog to reload. Defaults to None.
        """
        if cog is not None:
            try:
                self.bot.reload_extension("cogs." + cog)
                await say(ctx, f"The {cog} cog was reloaded.")
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                await say(ctx, "Something went wrong...")

    @cog_subcommand(
        base="manage",
        description="Load a new cog.",
        guild_ids=guild_ids,
        options=[create_option("cog", "The cog to load.", opt.STRING, True)])
    async def load(self, ctx: ctx, cog: str = None):
        """Load a new cog.

        Args:
            cog (str, optional): The cog to load. Defaults to None.
        """
        if cog is not None:
            try:
                self.bot.load_extension("cogs." + cog)
                await say(ctx, f"The {cog} cog was loaded.")
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                await say(ctx, "Something went wrong...")

    @cog_subcommand(
        base="manage",
        description="Unload an existing cog.",
        guild_ids=guild_ids,
        options=[create_option("cog", "The cog to unload.", opt.STRING, True)])
    async def unload(self, ctx: ctx, cog: str = None):
        """Unload an existing cog.

        Args:
            cog (str, optional): The cog to unload. Defaults to None.
        """
        if cog is not None:
            try:
                self.bot.unload_extension("cogs." + cog)
                await say(ctx, f"Alright, the {cog} cog was unloaded.")
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                await say(ctx, "Something went wrong...")

    @cog_subcommand(base="manage", guild_ids=guild_ids)
    async def exit(self, ctx: ctx):
        """Take a break and shut down."""
        await say(ctx, "Sure, I'll see you later.")
        await self.bot.close()
        print("Client closed.")


def setup(bot: Bot):
    bot.add_cog(Manage(bot))
