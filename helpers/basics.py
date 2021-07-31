from discord import Activity, ActivityType, Color, Embed, TextChannel
from discord.ext.commands import Bot
from helpers.snek import snekkify


async def playing(bot: Bot, type: str, phrase: str):
    types = {
        "playing": ActivityType.playing,
        "streaming": ActivityType.streaming,
        "listening": ActivityType.listening,
        "watching": ActivityType.watching
    }
    activity = Activity(name=phrase, type=types[type])
    await bot.change_presence(activity=activity)


async def say(channel: TextChannel, message: str):
    embed = Embed(description=snekkify(message), color=Color.orange())
    await channel.send(embed=embed)
