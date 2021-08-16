from __main__ import settings
from discord import Color, Embed
from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext as ctx, ComponentContext as cctx
from discord_slash.cog_ext import cog_slash
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_actionrow, create_button, create_select, create_select_option
from helpers.basics import say
from helpers.snek import snekkify

guild_ids = settings["slash"]["guilds"]


class Component(Cog):

    listener = Cog.listener

    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_slash(guild_ids=guild_ids)
    async def buttons(self, ctx: ctx):
        """Want some buttons? We've got buttons."""
        buttons = [
            create_button(style=ButtonStyle.red,
                          label="A Red Button",
                          custom_id="red"),
            create_button(style=ButtonStyle.green,
                          label="A Green Button",
                          custom_id="green"),
            create_button(style=ButtonStyle.blue,
                          label="A Blue Button",
                          custom_id="blue"),
        ]
        action_row = create_actionrow(*buttons)

        await say(ctx, "You press the button?", components=[action_row])

    @listener("on_component")
    async def buttons_listener(self, ctx: cctx):
        embed = Embed(color=Color.orange())
        if ctx.custom_id == "red":
            embed.description = snekkify("Outstanding! Red button!")
            await ctx.edit_origin(embed=embed)
        elif ctx.custom_id == "green":
            embed.description = snekkify("Wow! Green button!")
            await ctx.edit_origin(embed=embed)
        elif ctx.custom_id == "blue":
            embed.description = snekkify("Sublime! Blue button!")
            await ctx.edit_origin(embed=embed)

    @cog_slash(guild_ids=guild_ids)
    async def selects(self, ctx: ctx):
        """Selections? We have selections."""
        select = create_select(
            options=[
                create_select_option("Lab Coat", value="coat", emoji="🥼"),
                create_select_option("Test Tube", value="tube", emoji="🧪"),
                create_select_option("Petri Dish", value="dish", emoji="🧫"),
            ],
            placeholder=snekkify("Select your science."),
            min_values=1,
            max_values=3,
            custom_id="science",
        )

        await say(ctx, "Science?", components=[create_actionrow(select)])

    @listener("on_component")
    async def selects_listener(self, ctx: cctx):
        embed = Embed(color=Color.orange())
        if ctx.custom_id == "science":
            embed.description = snekkify(
                f"Wow, {' and '.join(ctx.selected_options)}!")
            await ctx.edit_origin(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Component(bot))
