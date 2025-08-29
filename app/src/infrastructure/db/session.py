from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.src.infrastructure.db.models.tag_model import TagModel
from app.src.infrastructure.db.models.room_model import RoomModel
from app.src.infrastructure.db.models.building_model import BuildingModel 

from app.src.presentation.core.config import settings

engine = create_engine(settings.database_url.encoded_string(), echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session