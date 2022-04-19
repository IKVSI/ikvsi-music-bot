import logging
from typing import Tuple, Union
from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import StateFilter, Command
from aiogram.utils.helper import ListItem
from aiogram.utils import markdown

from .settings import TelegramSettings
from .templates import Templates
from .states import States


def commands(telegram_settings: TelegramSettings) -> Tuple[Bot, Dispatcher]:
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

        @self.register(commands=["start", "clear"])
        async def start(message: types.Message):
            state = self.dispatcher.current_state(user=message.from_user.id)
            await state.set_state(States.INIT[0])
            await message.answer(Templates.greeting)

        start.description = "Сброс бота в начальное состояние init"

        @self.register(commands=["help"])
        async def help(message: types.Message):
            commands_info = []
            for handler in self.dispatcher.message_handlers.handlers:
                func_commands = []
                correct = False
                for filter_object in handler.filters:
                    if isinstance(filter_object.filter, StateFilter):
                        correct = await filter_object.filter.check(message)
                    if isinstance(filter_object.filter, Command):
                        func_commands = filter_object.filter.commands
                if correct:
                    func = handler.handler
                    commands_info.append(
                        Templates.help_commands_info.format(
                            commands=", ".join(
                                f"/{command}" for command in func_commands
                            ),
                            description=getattr(
                                func, "description", "Хрен знает что делает"
                            ),
                        )
                    )
            answer = markdown.text(
                Templates.help_info.format(
                    state=await self.dispatcher.current_state(
                        user=message.from_user.id
                    ).get_state(),
                    commands_info="\n    • {}".format("\n    • ".join(commands_info)),
                )
            )
            await message.answer(answer, parse_mode=types.ParseMode.MARKDOWN)

        help.description = "Показывает возможные команды в текущем состоянии"


class AllCommands(Commands):
    def __init__(self, dispatcher):
        super().__init__(state=States.all(), dispatcher=dispatcher)

    def initCommands(self):
        self.handler = self.dispatcher.message_handler

        @self.register(commands=["state"])
        async def state_info(message: types.Message):
            state = self.dispatcher.current_state(user=message.from_user.id)
            await message.answer(
                Templates.state_info.format(state=await state.get_state())
            )

        state_info.description = "Показывает текущее состояние"
