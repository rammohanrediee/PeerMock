from asyncio import timeout
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from peermock.api.errors import ErrorResponse
from peermock.core.errors import DomainError
from peermock.db.session import get_db_session


class HealthResponse(BaseModel):
    status: Literal["ok"]


DatabaseSession = Annotated[AsyncSession, Depends(get_db_session)]

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/live",
    response_model=HealthResponse,
    summary="Check whether the API process is alive",
)
def liveness() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/ready",
    response_model=HealthResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
        }
    },
    summary="Check whether the API is ready to serve requests",
)
async def readiness(session: DatabaseSession) -> HealthResponse:
    try:
        async with timeout(2):
            database_answer = await session.scalar(text("SELECT 1"))
    except (TimeoutError, SQLAlchemyError) as error:
        raise DomainError(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="database_unavailable",
            message="Database is unavailable",
        ) from error

    if database_answer != 1:
        raise DomainError(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="database_unavailable",
            message="Database is unavailable",
        )

    return HealthResponse(status="ok")
