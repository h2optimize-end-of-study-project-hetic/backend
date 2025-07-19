import logging
import pytest
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Session


from app.src.presentation.main import app
from app.src.presentation.core.config import settings
from app.src.infrastructure.db.session import get_session


logger = logging.getLogger(__name__)
test_db_name = f"{settings.POSTGRES_DB}_test"
test_db_url = sqlalchemy.URL.create(
    "postgresql+psycopg2",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=test_db_name,
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():

    print("Setup intégration test")

    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine.Engine')
    sqlalchemy_logger.setLevel(logging.WARNING)
    sqlalchemy_logger.propagate = False 

    admin_url = sqlalchemy.URL.create(
        "postgresql+psycopg2",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database="postgres",
    )
    

    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

    with admin_engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        conn.execute(text(f"CREATE DATABASE {test_db_name}"))
        print(f"DB {test_db_name} created\n")


    test_engine = create_engine(test_db_url, echo=True, future=True)
    SQLModel.metadata.create_all(test_engine)

    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    yield

    with admin_engine.connect() as conn:
        conn.execute(text(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{test_db_name}' AND pid <> pg_backend_pid();
        """))

        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        print(f"\nDB {test_db_name} deleted")


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    engine = create_engine(test_db_url, echo=False, future=True)

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    yield