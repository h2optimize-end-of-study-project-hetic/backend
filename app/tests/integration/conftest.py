from datetime import datetime, timedelta
import os
import pytest
import logging
from jose import jwt


from alembic import command
from sqlmodel import SQLModel
from alembic.config import Config
from sqlmodel import Session
from sqlalchemy import create_engine, text

from app.src.presentation.core.config import settings
from app.src.domain.entities.role import Role
from app.src.infrastructure.db.models.user_model import UserModel


test_db_name = f"{settings.POSTGRES_DB}_test"
test_db_url = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@postgres/{test_db_name}"


def modify_alembic_ini(original_ini_path: str, new_url: str) -> str:
    temp_ini_path = "/code/app/alembic_test.ini"
    with open(original_ini_path) as f_src, open(temp_ini_path, "w") as f_dst:
        for line in f_src:
            if line.strip().startswith("sqlalchemy.url"):
                f_dst.write(f"sqlalchemy.url = {new_url}\n")
            else:
                f_dst.write(line)
    return temp_ini_path


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    sqlalchemy_logger = logging.getLogger("sqlalchemy")
    sqlalchemy_logger.setLevel(logging.WARNING)
    sqlalchemy_logger.propagate = False

    print("=== Setup test env")
    admin_url = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@postgres/postgres"
    engine_admin = create_engine(admin_url, isolation_level="AUTOCOMMIT")

    with engine_admin.connect() as conn:
        print("1. Remove old DB")
        conn.execute(
            text(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{test_db_name}' AND pid <> pg_backend_pid();
        """)
        )
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        print("2. Create new DB")
        conn.execute(text(f"CREATE DATABASE {test_db_name}"))
        print("3. Setup DB test")

    original_ini_path = "/code/app/alembic.ini"
    temp_ini_path = modify_alembic_ini(original_ini_path, test_db_url)
    alembic_cfg = Config(temp_ini_path)

    try:
        print("4. Start migration")
        command.upgrade(alembic_cfg, "head")
        print("5. Migration end")
    finally:
        os.remove(temp_ini_path)

    yield

    with engine_admin.connect() as conn:
        print("\n\n6. Remove DB")
        conn.execute(
            text(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{test_db_name}' AND pid <> pg_backend_pid();
        """)
        )
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        print("7. DB deleted")


test_engine = create_engine(test_db_url)


def get_test_session():
    with Session(test_engine) as session:
        yield session


@pytest.fixture(autouse=True)
def clean_db():
    with Session(test_engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.exec(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;'))
        session.commit()
        yield


@pytest.fixture
def test_user():
    """
    Crée un utilisateur en base pour les tests.
    Mot de passe = 1234 (hash déjà connu).
    """
    hashed_password = "$2b$12$A8IR/uZfnys3kvMmDP1PJuvJwKaqoUXD5brPDoRvxyTWXg2xuoo7W"

    user = UserModel(
        email="testuser@example.com",
        salt="testsalt",  # valeur bidon mais non NULL
        password=hashed_password,
        secret_2fa=None,  # si NOT NULL en DB, mettre une chaîne vide ""
        firstname="John",
        lastname="Doe",
        phone_number="0600000000",
        role=Role.admin.value,
        is_active=True,
        is_delete=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    with Session(test_engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@pytest.fixture
def auth_headers(test_user):
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(test_user.id),
        "email": test_user.email,
        "role": test_user.role,
        "exp": expire,
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"Authorization": f"Bearer {token}"}