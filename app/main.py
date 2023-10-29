import logging.config

import sentry_sdk
from fastapi import FastAPI

from app.api import routes
from app.middlewares import PaginationMiddleware
from app.settings import settings


def create_app():
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.sentry_environment or None,
        )

    logging.config.dictConfig(settings.logging)

    app = FastAPI()
    app.add_middleware(PaginationMiddleware)
    app.include_router(router=routes.router, prefix="/api")

    return app


app = create_app()
