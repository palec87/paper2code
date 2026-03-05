"""Database configuration helpers for the registry backends."""

import os


def get_database_url() -> str:
    """Return configured PostgreSQL URL or a sensible local default."""
    return os.getenv(
        "PAPER2CODE_DB_URL",
        "postgresql+psycopg://paper2code:paper2code@localhost/paper2code",
    )
