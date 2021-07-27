from helpers import startup

if __name__ == "__main__":
    settings = startup.get_settings("noodle")
    bot = startup.instantiate_bot(settings)

    extensions = startup.get_extensions(settings["optional_cogs"],
                                        settings["excluded_cogs"],
                                        settings["external_cogs"])
    [bot.load_extension(extension) for extension in extensions]

    token = startup.get_token()

    try:
        bot.loop.run_until_complete(bot.start(token, bot=True, reconnect=True))
    finally:
        bot.loop.close()
