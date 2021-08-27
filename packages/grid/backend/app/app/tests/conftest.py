# stdlib
import asyncio
import logging

# third party
from _pytest.logging import LogCaptureFixture
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from loguru import logger
import pytest

# syft absolute
from syft.core.node.common.node_table.utils import seed_db

# grid absolute
from app.core.config import settings
from app.db.session import SessionLocal
from app.db.session import engine
from app.logger.handler import get_log_handler

from syft.core.node.common.node_table import Base  # noqa


log_handler = get_log_handler()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def _caplog(caplog: LogCaptureFixture) -> LogCaptureFixture:
    class PropagateHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            logging.getLogger(record.name).handle(record)

    sink_handler_id = logger.add(PropagateHandler(), format=log_handler.format_record)
    yield caplog
    logger.remove(sink_handler_id)


@pytest.fixture(scope="session")
async def app() -> FastAPI:
    # grid absolute
    from app.main import app

    async with LifespanManager(app):
        yield app


@pytest.fixture(scope="session")
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url=settings.SERVER_HOST,
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture(autouse=True)
async def load_db() -> None:
    db = SessionLocal()
    Base.metadata.create_all(engine)
    seed_db(db)
