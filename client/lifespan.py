from contextlib import asynccontextmanager
import logging
from api.broker import broker

from fastapi import FastAPI

from db.session import init_db

@asynccontextmanager
async def start_app(app: FastAPI):
    await broker.start()
    await init_db()
    logging.info("start app")
    yield
    await broker.stop()
    logging.info("app close")