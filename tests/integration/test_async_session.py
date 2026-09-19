"""Opt-in verification of the application's async PostgreSQL session lifecycle."""

import asyncio
import os

import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from peermock.db.session import engine, get_db_session

pytestmark = pytest.mark.skipif(
    os.environ.get("PEERMOCK_RUN_DB_TESTS") != "1",
    reason="Set PEERMOCK_RUN_DB_TESTS=1 to check the local database session",
)


def test_async_session_connects_and_cleans_up() -> None:
    async def verify_session() -> None:
        assert engine.url.drivername == "postgresql+psycopg"
        assert engine.url.host in {"localhost", "127.0.0.1", "::1"}
        assert engine.url.database == "peermock"

        dependency = get_db_session()
        session = await anext(dependency)
        try:
            try:
                assert await session.scalar(text("SELECT 1")) == 1
            except SQLAlchemyError:
                pytest.fail(
                    "Local PostgreSQL connection failed; verify the service and sanitized settings",
                    pytrace=False,
                )
            assert session.in_transaction()
        finally:
            await dependency.aclose()
            await engine.dispose()

        assert not session.in_transaction()

    asyncio.run(verify_session())
