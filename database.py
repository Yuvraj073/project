from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings


engine = create_engine(settings.database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def check_database_connection() -> None:
    """Run a minimal query to verify that PostgreSQL is reachable."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
