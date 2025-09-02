from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.src.infrastructure.db.models.tag_model import TagModel
from app.src.infrastructure.db.models.room_model import RoomModel
from app.src.infrastructure.db.models.building_model import BuildingModel 

from app.src.presentation.core.config import settings

engine_main = create_engine(settings.database_url, echo=True)
engine_recorded = create_engine(settings.database_recorded_url, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine_main) as session:
        yield session

def get_session_recorded() -> Generator[Session, None, None]:
    with Session(engine_recorded) as session:
        yield session