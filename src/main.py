import logging
from aiogram import executor
from bot import commands, TelegramSettings


def main():
    logging.basicConfig(level=logging.INFO)
    telegram_settings = TelegramSettings()
    bot, dispatcher = commands(telegram_settings)
    executor.start_polling(dispatcher)


if __name__ == "__main__":
    main()
