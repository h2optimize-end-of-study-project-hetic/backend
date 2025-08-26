import logging
import pytest
import builtins

from fastapi.testclient import TestClient
from dateutil.parser import parse as parse_datetime

from app.src.domain.entities.room import Room
from app.src.presentation.main import app
from app.src.domain.entities.tag import Tag
from app.src.presentation.core.config import settings


logger = logging.getLogger(__name__)

original_print = print

def print(*args, **kwargs):  # noqa: A001
    text = " ".join(str(arg) for arg in args)
    colored_text = f"\033[1;34m{text}\033[0m"
    original_print(colored_text, **kwargs)


builtins.print = print

@pytest.fixture(autouse=True, scope="session")
def disable_info_logs_for_tests():
    """
    Limit noise from logger
    """
    settings.LOG_LEVEL = "WARNING"
    logging.getLogger().setLevel(logging.WARNING)

    logger.warning("LOG_LEVEL change to WARNING")

    for logger_name in logging.root.manager.loggerDict:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


@pytest.fixture(scope="session")
def client():
    """
    Fournit un client TestClient FastAPI lié à la base de test.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_tags_factory():
    """
    Factory pour générer une liste de Tags de test.
    Usage : sample_tags_factory(start, end)
    """

    def _factory(start: int, end: int):
        return [
            Tag(
                id=i,
                name=f"Tag {i}",
                description="desc",
                source_address=f"addr_{i}",
                created_at=parse_datetime("2025-07-17T20:14:19.947"),
                updated_at=parse_datetime("2025-07-17T20:14:19.947"),
            )
            for i in range(start, end)
        ]

    return _factory



@pytest.fixture
def sample_rooms_factory():
    """
    Factory pour générer une liste de Rooms de test.
    Usage : sample_rooms_factory(start, end)
    """

    def _factory(start: int, end: int):
        return [
            Room(
                id=i,
                name=f"Room {i}",
                description="desc",
                floor=i,
                building_id=1,
                area=i,
                shape=[[i*2], [i*1]],
                capacity=i,
                created_at=parse_datetime("2025-07-17T20:14:19.947"),
                updated_at=parse_datetime("2025-07-17T20:14:19.947"),
                start_at=parse_datetime("2025-07-17T20:14:19.947"),
                end_at=parse_datetime("2025-07-17T21:14:19.947"),
            )
            for i in range(start, end)
        ]

    return _factory