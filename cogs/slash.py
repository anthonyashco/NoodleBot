from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext
from discord_slash.cog_ext import cog_slash
from helpers.basics import say
import yaml

guild_ids = None

try:
    with open("settings.yml", "r") as f:
        settings = yaml.safe_load(f)
        guild_ids = settings["noodle"]["slash"]["guilds"]
except FileNotFoundError:
    print("No settings.yml present.")


class Slash(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_slash(name="ping", guild_ids=guild_ids)
    async def ping(self, ctx: SlashContext):
        await say(ctx.channel, f"Pong! ({self.bot.latency*1000}ms)")


def setup(bot: Bot):
    bot.add_cog(Slash(bot))
