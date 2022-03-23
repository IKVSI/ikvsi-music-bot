from pydantic import BaseSettings
from pydantic import SecretStr
from aiogram import Dispatcher, Bot


class TelegramSettings(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_prefix = "TELEGRAM_"
