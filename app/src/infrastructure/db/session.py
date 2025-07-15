from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.src.presentation.core.config import settings

engine = create_engine(settings.database_url.encoded_string(), echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session