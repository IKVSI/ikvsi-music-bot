import logging
from bot import TelegramSettings
from aiogram import executor
from bot.state_controller import StateController


def main():
    logging.basicConfig(level=logging.INFO)
    telegram_settings = TelegramSettings()
    sc = StateController(telegram_settings)
    executor.start_polling(sc.dispatcher)


if __name__ == "__main__":
    main()
