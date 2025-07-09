from contextlib import contextmanager
from sqlmodel import Session, create_engine


DATABASE_URL = "postgresql+psycopg2://admin:Changeme!1@postgres:5432/app"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()