from pydantic import BaseSettings
from aiogram.utils import markdown
from aiogram import types


class Templates:
    greeting: str = "Привет @{user_name}, Я музыкальный бот @{bot_name}! Хочешь создать свою музыкальную библиотеку?"
    greeting_for_old: str = "Привen @{user_name}, пришёл послушать музыку?"
    reset: str = "@{user_name}, произошёл сброс в исходное состояние."
    state_info: str = "Твоё текущее состояние {state}!"
    help_commands_info: str = "{commands} - {description}"
    help_info: str = "В состоянии {state} работают команды: {commands_info}"
