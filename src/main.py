import logging
from typing import Tuple

from aiogram import executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.settings import TelegramSettings
from bot.db.settings import DataBaseSettings
from bot.commands.commands import Commands
from bot.commands.overstate import OverstateCommands
from bot.commands.root import RootCommands
from bot.commands.music import MusicCommands


def prepare_bot() -> Tuple[Bot, Dispatcher]:
    telegram_settings = TelegramSettings()
    database_settings = DataBaseSettings()
    bot = Bot(token=telegram_settings.bot_token.get_secret_value())
    Commands.dispatcher = Dispatcher(bot, storage=MemoryStorage())
    Commands.engine = create_async_engine(
        database_settings.url.format(driver="postgresql+asyncpg"), echo=True
    )
    Commands.async_session = sessionmaker(Commands.engine, class_=AsyncSession)
    Commands.storage_chat_id = telegram_settings.storage_chat_id
    list_commands = [OverstateCommands, RootCommands]
    list_commands.extend(MusicCommands)
    for commands in list_commands:
        commands()
    return (bot, Commands.dispatcher)


def main():
    logging.basicConfig(level=logging.INFO)
    bot, dispatcher = prepare_bot()
    executor.start_polling(dispatcher)


if __name__ == "__main__":
    main()
