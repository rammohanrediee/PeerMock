"""FastAPI application composition."""

from fastapi import FastAPI

from peermock.api.errors import domain_error_handler
from peermock.api.router import router as api_router
from peermock.core.config import settings
from peermock.core.errors import DomainError


def create_app() -> FastAPI:
    """Create and configure the PeerMock ASGI application."""

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )
    application.add_exception_handler(DomainError, domain_error_handler)
    application.include_router(api_router)
    return application


app = create_app()
