from .settings import TelegramSettings
from aiogram import types
from aiogram import executor
from aiogram import Bot, Dispatcher


class StateController:
    def __init__(self, telegram_settings: TelegramSettings):
        self._tg_settings = telegram_settings
        self.bot = Bot(telegram_settings.bot_token.get_secret_value())
        self.dispatcher = Dispatcher(self.bot)
        self.register()

    def register(self):
        @self.dispatcher.message_handler()
        async def send_welcome(message: types.Message):
            """
            This handler will be called when user sends `/start` or `/help` command
            """
            await message.reply("HELL!")
