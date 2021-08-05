from __main__ import settings
from discord import Color, Embed
from discord.errors import NotFound
from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext as ctx
from discord_slash.cog_ext import cog_slash
from discord_slash.model import SlashCommandOptionType as opt
from discord_slash.utils.manage_commands import create_option
from helpers.basics import say
from helpers.snek import snekkify
import random
import re
import requests

guild_ids = settings["slash"]["guilds"]


def text_loader(file_path: str):
    items = []
    try:
        with open(file_path, "r") as f:
            for i in f:
                items.append(i.strip())
        return items
    except FileNotFoundError:
        print(f"{file_path} not found.")


class Meme(Cog):

    listener = Cog.listener

    def __init__(self, bot: Bot):
        self.bot = bot
        self.swears = text_loader("data/swears_full.txt")
        self.pokemon = text_loader("data/pokemon_names.txt")

    @cog_slash(guild_ids=guild_ids,
               options=[
                   create_option("query", "The integer to query", opt.INTEGER,
                                 True)
               ])
    async def is_even(self, ctx: ctx, query: int):
        """Check if an integer is even using isevenapi."""
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
        await say(ctx, message)

    @listener("on_message")
    async def poke_swears(self, message):

        def replace(match):
            word = match.group()
            if word.lower() in self.swears:
                return random.choice(self.pokemon).upper()
            else:
                return word

        # TODO: Export to check.
        if message.channel.name == "bot-spam":
            try:
                text = re.sub(r"\b\w*\b", replace, message.content, flags=re.I)
                if message.content != text:
                    await message.delete()
                    author = message.author
                    embed = Embed(description=snekkify(text),
                                  color=Color.orange())
                    embed.set_author(
                        name=f"{author.display_name} ({message.author})",
                        icon_url=author.avatar_url)
                    await message.channel.send(embed=embed)
            except NotFound:
                print("Message not found.")


def setup(bot: Bot):
    bot.add_cog(Meme(bot))
