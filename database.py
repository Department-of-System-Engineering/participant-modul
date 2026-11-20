import psycopg2
import psycopg2.extras
from contextlib import contextmanager

async def init_db():
    pass

async def close_db():
    pass

@contextmanager
def get_db():
    conn = psycopg2.connect(
        database="participant_modul",
        user="postgres",
        password="postgres",
        host="db",
        port="5432",
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