from discord import Color, Embed, TextChannel
from helpers.snek import snekkify


async def say(channel: TextChannel, message: str):
    embed = Embed(description=snekkify(message), color=Color.orange())
    await channel.send(embed=embed)
