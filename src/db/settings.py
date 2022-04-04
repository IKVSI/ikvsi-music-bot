from pydantic import BaseSettings, SecretStr


class DataBaseSettings(BaseSettings):
    db: SecretStr
    user: SecretStr
    password: SecretStr
    host: SecretStr = "0.0.0.0"
    port: SecretStr = "5432"

    class Config:
        env_prefix = "POSTGRES_"

    @property
    def url(self):
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            user=self.user.get_secret_value(),
            password=self.password.get_secret_value(),
            host=self.host.get_secret_value(),
            port=self.port.get_secret_value(),
            database=self.db.get_secret_value(),
        )
