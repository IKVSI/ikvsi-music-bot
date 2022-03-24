from typing import Callable

from aiogram import types, Bot, Dispatcher
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted
from .states import States
from .settings import TelegramSettings
import logging


async def echo(message: types.Message):
    await message.reply(message.message_id)

class CommandsController():
    def __init__(self, telegram_settings: TelegramSettings):
        self._tg_settings = telegram_settings
        self._bot = Bot(token=self._tg_settings.bot_token.get_secret_value())
        self._dispatcher = Dispatcher(self._bot)
        self.register_command(
            handler=self.dispatcher.message_handler,
            func=echo,
            state="*",
            commands=["start", "restart"]
        )

    @staticmethod
    def register_command(handler: Callable, func: Callable, **kwargs):
        handler(**kwargs)(func)

    @property
    def bot(self):
        return self._bot
    @property
    def dispatcher(self):
        return self._dispatcher
