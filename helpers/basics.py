from discord import Activity, ActivityType, Color, Embed, TextChannel
from discord.ext.commands import Bot
from discord_slash import SlashContext
from helpers.snek import snekkify
from typing import Union


async def playing(bot: Bot, type: str, phrase: str):
    types = {
        "playing": ActivityType.playing,
        "streaming": ActivityType.streaming,
        "listening": ActivityType.listening,
        "watching": ActivityType.watching
    }
    activity = Activity(name=phrase, type=types[type])
    await bot.change_presence(activity=activity)


async def say(ctx: Union[TextChannel, SlashContext],
              message: str,
              hidden: bool = False):
    embed = Embed(description=snekkify(message), color=Color.orange())
    if type(ctx) == SlashContext:
        await ctx.send(embed=embed, hidden=hidden)
    elif type(ctx) == TextChannel:
        await ctx.send(embed=embed)
    else:
        raise TypeError
