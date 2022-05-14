from pydantic import BaseSettings
from pydantic import SecretStr


class TelegramSettings(BaseSettings):
    bot_token: SecretStr
    storage_chat_id: SecretStr

    class Config:
        env_prefix = "TELEGRAM_"
