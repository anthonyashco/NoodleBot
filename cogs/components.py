from __main__ import settings
from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext as ctx, ComponentContext as cctx
from discord_slash.cog_ext import cog_slash
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_actionrow, create_button, create_select, create_select_option, wait_for_component
from helpers.basics import say
from helpers.snek import snekkify

guild_ids = settings["slash"]["guilds"]


class Component(Cog):

    listener = Cog.listener

    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_slash(guild_ids=guild_ids)
    async def buttons(self, ctx: ctx):
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

        await ctx.send(snekkify("You press the button?"),
                       components=[action_row])

    @listener("on_component")
    async def buttons_listener(self, ctx: cctx):
        if ctx.custom_id == "red":
            await ctx.edit_origin(content=snekkify("Outstanding! Red button!"))
        elif ctx.custom_id == "green":
            await ctx.edit_origin(content=snekkify("Wow! Green button!"))
        elif ctx.custom_id == "blue":
            await ctx.edit_origin(content=snekkify("Sublime! Blue button!"))

    @cog_slash(guild_ids=guild_ids)
    async def selects(self, ctx: ctx):
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

        await ctx.send(snekkify("Science?"),
                       components=[create_actionrow(select)])

    @listener("on_component")
    async def selects_listener(self, ctx: cctx):
        if ctx.custom_id == "science":
            await ctx.edit_origin(
                content=snekkify(f"Wow, {' and '.join(ctx.selected_options)}!"))


def setup(bot: Bot):
    bot.add_cog(Component(bot))
