from discord_slash import SlashCommand
from helpers import startup

if __name__ == "__main__":
    settings = startup.get_settings("noodle")
    connect = startup.get_settings("mongo_connect")
    bot = startup.instantiate_bot(settings)
    slash = SlashCommand(bot, sync_commands=True)
    token = startup.get_token()

    extensions = startup.get_extensions(settings["optional_cogs"],
                                        settings["excluded_cogs"],
                                        settings["external_cogs"])
    [bot.load_extension(extension) for extension in extensions]

    try:
        bot.loop.run_until_complete(bot.start(token, bot=True, reconnect=True))
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Goodbye!")
    finally:
        bot.loop.close()
