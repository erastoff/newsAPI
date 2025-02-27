from functools import lru_cache
from typing import final

from decouple import config
from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".prod.env", ".dev.env"),  # first search .dev.env, then .prod.env
        env_file_encoding="utf-8",
    )
    debug: bool = config("DEBUG")

    db_name: str = config("DATABASE_NAME")
    db_user: str = config("DATABASE_USER")
    db_password: str = config("DATABASE_PASSWORD")
    db_host: str = config("DATABASE_HOST")
    db_port: str = config("DATABASE_PORT")
    db_url: str = f"postgresql+asyncpg://{db_user}:{db_password}@db:{db_port}/{db_name}"


@lru_cache()  # get it from memory
def get_settings() -> Settings:
    return Settings()
