from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str

    @field_validator("database_url")
    @classmethod
    def require_postgresql_psycopg(cls, value: str) -> str:
        """Reject URLs that do not use PostgreSQL through Psycopg 3."""
        try:
            drivername = make_url(value).drivername
        except Exception as exc:
            raise ValueError("DATABASE_URL must be a valid SQLAlchemy URL") from exc

        if drivername != "postgresql+psycopg":
            raise ValueError(
                "DATABASE_URL must use the postgresql+psycopg:// scheme"
            )
        return value


settings = Settings()
