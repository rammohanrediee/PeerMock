"""Tests for the shared domain-error HTTP contract."""

from fastapi import status
from fastapi.testclient import TestClient

from peermock.core.errors import DomainError
from peermock.main import create_app


def test_domain_error_uses_stable_public_response() -> None:
    application = create_app()

    @application.get("/test/domain-error")
    def raise_domain_error() -> None:
        raise DomainError(
            status_code=status.HTTP_409_CONFLICT,
            code="booking_conflict",
            message="The slot is no longer available",
        )

    with TestClient(application) as client:
        response = client.get("/test/domain-error")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "code": "booking_conflict",
        "message": "The slot is no longer available",
    }
