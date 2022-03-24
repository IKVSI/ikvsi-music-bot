import logging
from bot import TelegramSettings
from aiogram import executor
from bot import CommandsController

def main():
    logging.basicConfig(level=logging.INFO)
    telegram_settings = TelegramSettings()
    sc = CommandsController(telegram_settings)
    executor.start_polling(sc.dispatcher)

if __name__ == "__main__":
    main()
