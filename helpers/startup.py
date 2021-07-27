from discord.ext.commands import Bot
from typing import Dict, List
import discord
import os
import yaml


def get_extensions(optional_cogs: List[str] = [],
                   excluded_cogs: List[str] = [],
                   external_cogs: List[str] = []) -> List[str]:
    """Check cog folders and return a list of extensions to load."""
    if optional_cogs is None:
        optional_cogs = []
    if excluded_cogs is None:
        excluded_cogs = []
    if external_cogs is None:
        external_cogs = []

    extensions_list = []

    try:
        cogs = os.listdir("cogs")
        for cog in cogs:
            if (cog.endswith(".py") and
                    cog.partition(".py")[0] not in excluded_cogs):
                cog = "cogs." + cog.partition(".py")[0]
                extensions_list.append(cog)
    except FileNotFoundError:
        print("No /cogs directory detected.")

    try:
        cogs_optional = os.listdir("cogs_optional")
        for cog in cogs_optional:
            if (cog.endswith(".py") and
                    cog.partition(".py")[0] in optional_cogs):
                cog = "cogs_optional." + cog.partition(".py")[0]
                extensions_list.append(cog)
    except FileNotFoundError:
        print("No /cogs_optional directory detected.")

    try:
        for cog in external_cogs:
            if cog.endswith(".py"):
                extensions_list.append(cog)
    except FileNotFoundError:
        print(f"{cog} not found.")

    return extensions_list


def get_settings(setting: str = None):
    """Check for a settings.json file that has Noodle's settings."""

    try:
        with open("settings.yml", "r") as file:
            settings = yaml.safe_load(file)
        if setting is not None:
            return settings[setting]
        else:
            return settings

    except FileNotFoundError:
        print("No settings.yml present.")
        exit()


def get_token():
    """Check for a token.yml file that has Noodle's login token."""

    try:
        with open("token.yml", "r") as file:
            token = yaml.safe_load(file)
        return token

    except FileNotFoundError:
        print("No token.yml present.")
        exit()


def instantiate_bot(settings: Dict) -> Bot:
    """Instantiates the bot."""

    def set_intents():
        """Prepare Intents object."""

        print("Preparing intents")
        intents = discord.Intents.none()
        intents.guilds = True
        intents.members = True
        intents.emojis = True
        intents.presences = True
        intents.messages = True
        intents.reactions = True
        return intents

    bot = Bot(
        command_prefix=settings["trigger"],
        case_insensitive=True,
        intents=set_intents(),
    )

    bot.settings = settings
    bot.owner_ids = {owner for owner in bot.settings["owners"]}

    return bot
