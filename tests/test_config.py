import pytest
from pydantic import ValidationError

from config import Settings


def test_settings_load_postgresql_psycopg_url_from_environment(monkeypatch):
    database_url = "postgresql+psycopg://user:secret@localhost:5432/jobtrack"
    monkeypatch.setenv("DATABASE_URL", database_url)

    settings = Settings(_env_file=None)

    assert settings.database_url == database_url


@pytest.mark.parametrize(
    "database_url",
    [
        "postgresql://user:secret@localhost:5432/jobtrack",
        "mysql+pymysql://user:secret@localhost:3306/jobtrack",
        "not-a-database-url",
    ],
)
def test_settings_reject_non_psycopg_database_urls(monkeypatch, database_url):
    monkeypatch.setenv("DATABASE_URL", database_url)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
