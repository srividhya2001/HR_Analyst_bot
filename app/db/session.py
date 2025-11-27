from sqlalchemy import create_engine, text
import pandas as pd
from app.core.config import settings


def get_engine():
    """
    Create a SQLAlchemy engine for PostgreSQL using application settings.
    """
    url = (
        f"postgresql+psycopg2://{settings.DB_USER}:"
        f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
        f"{settings.DB_PORT}/{settings.DB_NAME}"
    )

    engine = create_engine(
        url,
        connect_args={"options": "-c statement_timeout=3000"},
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=2
    )
    return engine


engine = get_engine()


def run_query(sql: str) -> pd.DataFrame:
    """
    Execute a validated SQL query and return the result as a DataFrame.
    """
    with engine.connect() as connection:
        df = pd.read_sql(text(sql), connection)
    return df