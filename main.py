import json
from os import environ

from telegram_bot.bot import TelegramBot

if __name__ == "__main__":
    settings_file_path = environ.get('settings_file_path') \
        if environ.get('settings_file_path') is not None else "settings.json"

    with open(settings_file_path) as settings_file:
        settings = json.load(settings_file)

    telegram_bot = TelegramBot(settings)
    telegram_bot.run()

