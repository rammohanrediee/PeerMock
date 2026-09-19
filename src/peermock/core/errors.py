"""Stable application errors raised by feature and core services."""


class DomainError(Exception):
    """Expected application failure safe to expose through the API."""

    def __init__(self, *, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
