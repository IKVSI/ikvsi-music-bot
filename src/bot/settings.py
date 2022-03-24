from pydantic import BaseSettings
from pydantic import SecretStr


class TelegramSettings(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_prefix = "TELEGRAM_"
