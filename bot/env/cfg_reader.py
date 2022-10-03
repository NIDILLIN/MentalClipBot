from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr


    class Config:
        env_file = 'bot/env/.env'
        env_file_encoding = 'utf-8'



config = Settings()