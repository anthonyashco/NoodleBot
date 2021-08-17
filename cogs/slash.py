from __main__ import settings, slash
from discord import Color, Embed
from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext as ctx
from discord_slash.cog_ext import cog_slash
from discord_slash.model import SlashCommandOptionType as opt
from helpers.basics import say

guild_ids = settings["slash"]["guilds"]


class Slash(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_slash(guild_ids=guild_ids)
    async def ping(self, ctx: ctx):
        """Check Noodle's latency."""
        await say(ctx, f"Pong! ({self.bot.latency*1000}ms)", hidden=True)

    @cog_slash(guild_ids=guild_ids)
    async def help(self, ctx: ctx):
        """Check the current commands."""
        commands = await slash.to_dict()
        guild = commands["guild"][ctx.guild_id]
        filtered = {}
        for x in guild:
            filtered[x["name"]] = {
                "description": x["description"],
                "options": {}
            }
            for option in x["options"]:
                if option["type"] == opt.SUB_COMMAND:
                    filtered[x["name"]]["options"][
                        option["name"]] = option["description"]
        message = []
        for k in sorted(filtered.keys()):
            v = filtered[k]
            message.append(f"{k}:" if v["description"] ==
                           "No Description." else f"{k}: {v['description']}")
            if len(v["options"]) > 0:
                for k_2, v_2 in v["options"].items():
                    message.append(f"  {k_2}: {v_2}")
        formatted = "```yaml\n" + "\n".join(message) + "```"
        embed = Embed(description=formatted, color=Color.orange())
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Slash(bot))
