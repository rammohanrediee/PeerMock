"""HTTP translation for stable application errors."""

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from peermock.core.errors import DomainError


class ErrorResponse(BaseModel):
    """Public error response shared by API endpoints."""

    code: str
    message: str


async def domain_error_handler(_: Request, error: Exception) -> JSONResponse:
    """Translate an expected domain failure without exposing internal details."""

    if not isinstance(error, DomainError):
        raise error

    response = ErrorResponse(code=error.code, message=error.message)
    return JSONResponse(
        status_code=error.status_code,
        content=response.model_dump(),
    )
