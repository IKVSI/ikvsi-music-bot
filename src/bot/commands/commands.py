from abc import ABC, abstractmethod
from typing import Callable

from aiogram import Dispatcher, types
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from ..db import base
from ..logs import get_logger
from ..templates import Templates


class Commands(ABC):
    dispatcher: Dispatcher = None
    engine: AsyncEngine = None
    async_session: sessionmaker = None
    storage_chat_id: SecretStr = None
    registered_commands: dict[str | None, dict[str, Callable]] = {None: {}}
    registered_waiters: dict[str | None, list[Callable]] = {None: []}

    def __init__(self, state: str):
        self.state = state
        self.handler = Commands.dispatcher.message_handler
        self.initHandlers()

    def register(self, **kwargs):
        logger = get_logger(self.register)
        if kwargs.get("commands"):
            logger.info(f"Commands: {kwargs['commands']} for state: {self.state}")
        elif kwargs.get("content_types"):
            logger.info(
                f"Get content: {kwargs['content_types']} for state: {self.state}"
            )
        else:
            logger.info(f"Get text for state: {self.state}")

        def wrapper(func):
            func.description = Templates.default_description
            if Commands.registered_commands.get(self.state) is None:
                Commands.registered_commands[self.state] = {}
                Commands.registered_waiters[self.state] = []
            if kwargs.get("commands"):
                commands = ", ".join(
                    "/{}".format(commands.replace("_", "\\_"))
                    for commands in kwargs.get("commands")
                )
                Commands.registered_commands[self.state][commands] = func
            else:
                Commands.registered_waiters[self.state].append(func)
            return self.handler(state=self.state, **kwargs)(func)

        return wrapper

    @classmethod
    def commands_for_state(cls, state) -> list[tuple[str, str]]:
        return [
            (commands, func.description)
            for commands, func in Commands.registered_commands[state].items()
        ]

    @classmethod
    def waiters_for_state(cls, state) -> list[str]:
        return [func.description for func in Commands.registered_waiters[state]]

    @abstractmethod
    def initHandlers(self):
        pass


class ChooseCommands(Commands):
    def __init__(self, statement, **kwargs):
        self.step = 20
        self.statement = statement
        super().__init__(**kwargs)
        self.initSpecialHandlers()

    def initSpecialHandlers(self):
        self.handler = Commands.dispatcher.message_handler

        @self.register(commands=["next"])
        async def next(message: types.Message):
            async with Commands.async_session() as session:
                session.execute(self.statement)

        @self.register(commands=["prev", "previous"])
        async def previous(message: types.Message):
            pass


