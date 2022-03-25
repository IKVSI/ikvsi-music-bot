import logging
from typing import Union, Callable
from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.helper import ListItem

from .settings import TelegramSettings
from .templates import Templates
from .states import States


def commands(telegram_settings: TelegramSettings) -> tuple[Bot, Dispatcher]:
    bot = Bot(token=telegram_settings.bot_token.get_secret_value())
    dispatcher = Dispatcher(bot, storage=MemoryStorage())
    for command in [OverstateCommands, AllCommands]:
        command(dispatcher=dispatcher)
    return (bot, dispatcher)


class Commands:
    def __init__(self, state: Union[ListItem, str], dispatcher: Dispatcher):
        self.state = state
        self.dispatcher = dispatcher
        self.handler = dispatcher.message_handler
        self.initCommands()

    def register(self, **kwargs):
        logging.info(f"state={self.state} ")
        return self.handler(state=self.state, **kwargs)

    def initCommands(self):
        pass


class OverstateCommands(Commands):
    def __init__(self, dispatcher):
        super().__init__(state="*", dispatcher=dispatcher)

    def initCommands(self):
        self.handler = self.dispatcher.message_handler

        @self.register(commands=["start"])
        async def start(message: types.Message):
            state = self.dispatcher.current_state(user=message.from_user.id)
            await state.set_state(States.INIT)
            await message.answer(Templates.greeting)


class AllCommands(Commands):
    def __init__(self, dispatcher):
        super().__init__(state=States.all(), dispatcher=dispatcher)

    def initCommands(self):
        @self.register(commands=["state"])
        async def state_info(message: types.Message):
            state = self.dispatcher.current_state(user=message.from_user.id)
            await message.answer(
                Templates.state_info.format(state=await state.get_state())
            )
