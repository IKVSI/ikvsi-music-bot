import logging
from aiogram import executor
from bot import commands, TelegramSettings
from db import DataBaseSettings


def main():
    logging.basicConfig(level=logging.INFO)
    telegram_settings = TelegramSettings()
    database_settings = DataBaseSettings()
    bot, dispatcher = commands(telegram_settings, database_settings)
    executor.start_polling(dispatcher)


if __name__ == "__main__":
    main()
