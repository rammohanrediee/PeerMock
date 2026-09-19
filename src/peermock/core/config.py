"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the PeerMock API."""

    model_config = SettingsConfigDict(
        env_prefix="PEERMOCK_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "PeerMock"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str


settings = Settings()
