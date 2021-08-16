from __main__ import settings
from discord import Color, Embed
from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext as ctx
from discord_slash.cog_ext import cog_subcommand
from discord_slash.model import SlashCommandOptionType as opt
from discord_slash.utils.manage_commands import create_option
from helpers.basics import say
from helpers.mongo import db
from motor.motor_asyncio import AsyncIOMotorCollection as Collection

guild_ids = settings["slash"]["guilds"]
coll: Collection = db.dictionary
base_permissions = {}


class Dictionary(Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_subcommand(base="dictionary",
                    base_desc="Dictionary group.",
                    base_default_permission=True,
                    base_permissions=base_permissions,
                    guild_ids=guild_ids,
                    options=[
                        create_option("key", "The key for this entry.",
                                      opt.STRING, True),
                        create_option("value", "The value for this entry.",
                                      opt.STRING, True),
                    ])
    async def put(self, ctx: ctx, key: str, value: str):
        """Add a new dictionary entry or update an existing one."""
        key = key.lower()
        entry = {"key": key, "value": value}
        result = await coll.replace_one({"key": key}, entry, upsert=True)
        if result.acknowledged:
            await say(ctx, f"The entry for {key} was added to the database.")
        else:
            await say(ctx, "Something is amiss...")

    @cog_subcommand(base="dictionary",
                    guild_ids=guild_ids,
                    options=[
                        create_option("key", "The key for this entry.",
                                      opt.STRING, True),
                    ])
    async def get(self, ctx: ctx, key: str):
        """Return the value for a dictionary key."""
        key = key.lower()
        req = {"key": key}
        document = await coll.find_one(req)
        if document is not None:
            embed = Embed(description=document["value"],
                          color=Color.orange(),
                          title=key)
            await ctx.send(embed=embed)
        else:
            await say(ctx, "Nothing is here.")

    @cog_subcommand(base="dictionary",
                    guild_ids=guild_ids,
                    options=[
                        create_option("key", "The key for the entry to remove.",
                                      opt.STRING, True),
                    ])
    async def delete(self, ctx: ctx, key: str):
        """Delete a dictionary entry."""
        key = key.lower()
        req = {"key": key}
        result = await coll.delete_one(req)
        if result.deleted_count > 0:
            await say(ctx, "Entry was deleted.")
        else:
            await say(ctx, "Nothing was there to delete.")

    @cog_subcommand(base="dictionary", guild_ids=guild_ids)
    async def list(self, ctx: ctx):
        """List all known dictionary keys."""
        documents = await coll.find().to_list(None)
        keys = [document["key"] for document in documents]
        if len(keys) > 0:
            embed = Embed(description=", ".join(sorted(keys)),
                          color=Color.orange(),
                          title="Dictionary Keys")
            await ctx.send(embed=embed)
        else:
            await say(ctx, "The dictionary is empty.")


def setup(bot: Bot):
    bot.add_cog(Dictionary(bot))
