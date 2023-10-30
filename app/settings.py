import os

from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = ""
    sentry_dsn: str = ""
    sentry_environment: str = ""
    logging_handlers: list[str] = ["console"]
    logging_level: str = "DEBUG"

    googletrans_service_urls: list[str] = ["translate.googleapis.com"]
    googletrans_raise_exception: bool = False
    googletrans_proxies: dict | None = None

    pagination_sort_desc: bool = False
    pagination_per_page: int = 10
    pagination_per_page_max: int = 100

    class Config:
        # Usage of .env file may be disabled by NO_DOT_ENV environment
        # variable to avoid confusions and errors with double reading and
        # extra variables when using Docker Compose or any other upper layer
        # that reads .env file.
        env_file = ".env" if not os.getenv("NO_DOT_ENV", "") else None
        env_file_encoding = "utf-8"

    @property
    def logging(self) -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "file": {
                    "format": "[%(asctime)s: %(levelname)s/%(name)s] %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "level": self.logging_level,
                    "class": "logging.StreamHandler",
                    "formatter": "file",
                },
            },
            "loggers": {
                "uvicorn": {
                    "level": "INFO",
                    "handlers": self.logging_handlers,
                    "propagate": True,
                },
                "app": {
                    "level": "DEBUG",
                    "handlers": self.logging_handlers,
                    "propagate": True,
                },
                "sqlalchemy.engine": {
                    "level": "DEBUG",
                    "handlers": self.logging_handlers,
                    "propagate": True,
                },
            },
        }


settings = Settings()
