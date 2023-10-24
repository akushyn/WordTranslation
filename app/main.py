from fastapi import FastAPI
from app.api import routes


def create_app():
    app = FastAPI()
    app.include_router(router=routes.router, prefix="/api")

    return app


app = create_app()
