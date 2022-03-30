from pydantic import BaseSettings
from aiogram.utils import markdown
from aiogram import types


class Templates:
    greeting: str = "Привет, Я бот!"
    state_info: str = "Твоё текущее состояние {state}!"
    help_commands_info: str = "{commands} - {description}"
    help_info: str = "В состоянии {state} работают команды: {commands_info}"
