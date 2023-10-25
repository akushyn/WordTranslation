import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = ""
    echo_sql: bool = False

    model_config = SettingsConfigDict(
        case_sensitive=False,
        # Usage of .env file may be disabled by NO_DOT_ENV environment
        # variable to avoid confusions and errors with double reading and
        # extra variables when using Docker Compose or any other upper layer
        # that reads .env file.
        env_file=".env" if not os.getenv("NO_DOT_ENV", "") else None,
        env_file_encoding="utf-8",
    )


settings = Settings()
