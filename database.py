import psycopg2
import psycopg2.extras
from contextlib import contextmanager
import os

async def init_db():
    """
    Called on application startup in FastAPI lifespan.
    No connection pool initialization is needed with psycopg2,
    as each request opens and closes its own connection.
    """
    pass

async def close_db():
    """
    Called on application shutdown in FastAPI lifespan.
    No cleanup is needed since connections are closed after each request.
    """
    pass

@contextmanager
def get_db():
    """
    Context manager that provides a database connection.

    Usage:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM demographics")

    - Automatically COMMITs on success
    - ROLLBACKs and re-raises the exception on error
    - Always closes the connection in the finally block

    Returns:
        psycopg2 connection with RealDictCursor,
        which returns rows as dictionaries instead of tuples
    """
    conn = psycopg2.connect(
        database=os.getenv("POSTGRES_DB", "participant_modul"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "participant-db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()