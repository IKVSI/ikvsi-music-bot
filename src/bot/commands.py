from typing import Tuple, Union
from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import StateFilter, Command
from aiogram.utils.helper import ListItem
from aiogram.utils import markdown
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from db import DataBaseSettings
from db.base import Users, Lists
from abc import ABC, abstractmethod

from logs import get_logger

from . import TelegramSettings
from . import Templates
from . import States


def commands(
    telegram_settings: TelegramSettings, database_settings: DataBaseSettings
) -> Tuple[Bot, Dispatcher]:
    bot = Bot(token=telegram_settings.bot_token.get_secret_value())
    dispatcher = Dispatcher(bot, storage=MemoryStorage())
    engine = create_async_engine(
        database_settings.url.format(driver="postgresql+asyncpg"), echo=True
    )
    for command in [OverstateCommands, AllCommands]:
        command(dispatcher=dispatcher, engine=engine)
    return (bot, dispatcher)


class Commands(ABC):
    def __init__(
        self, state: Union[ListItem, str], dispatcher: Dispatcher, engine: AsyncEngine
    ):
        self.state = state
        self.dispatcher = dispatcher
        self.engine = engine
        self.assync_session = sessionmaker(engine, class_=AsyncSession)
        self.handler = dispatcher.message_handler
        self.initCommands()

    def register(self, **kwargs):
        logger = get_logger(self.register)
        logger.info(f"Commands: {kwargs['commands']} for state: {self.state}")
        return self.handler(state=self.state, **kwargs)

    @abstractmethod
    def initCommands(self):
        pass


class OverstateCommands(Commands):
    def __init__(self, **kwargs):
        super().__init__(state="*", **kwargs)

    def initCommands(self):
        self.handler = self.dispatcher.message_handler

        @self.register(commands=["start"])
        async def start(message: types.Message):
            context = self.dispatcher.current_state(user=message.from_user.id)
            user = message.from_user
            state = await context.get_state()
            if (state is None) or (state == States.INIT[0]):
                async with self.assync_session() as session:

                    def sync(session):
                        result: Users = (
                            session.query(Users)
                            .where(user.id == Users.user_id)
                            .one_or_none()
                        )
                        if result:
                            if result.user_name != user.username:
                                result.user_name = user.username
                            return Templates.greeting_for_old
                        else:
                            session.add(Users(user_id=user.id, user_name=user.username))
                            session.commit()
                            session.add(Lists(list_name="Library", user_id=user.id))
                            return Templates.greeting

                    answer = await session.run_sync(sync)
                    await session.commit()
            else:
                answer = Templates.reset
            await context.set_state(States.INIT[0])
            await message.answer(
                answer.format(
                    user_name=user.username,
                    bot_name=(await self.dispatcher.bot.get_me()).username,
                )
            )

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
                                func, "description", "Хрен знает что делает :/"
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
    def __init__(self, **kwargs):
        super().__init__(state=States.all(), **kwargs)

    def initCommands(self):
        self.handler = self.dispatcher.message_handler

        @self.register(commands=["state"])
        async def state_info(message: types.Message):
            state = self.dispatcher.current_state(user=message.from_user.id)
            await message.answer(
                Templates.state_info.format(state=await state.get_state())
            )

        state_info.description = "Показывает текущее состояние"
