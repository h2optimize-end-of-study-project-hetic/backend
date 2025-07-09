from app.src.infrastructure.db.session import get_session
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.infrastructure.db.repositories.tag_repository_sql import SQLTagRepository
from sqlmodel import Session
from fastapi import Depends


def get_tag_repository(session: Session = Depends(get_session)) -> TagRepository:
    return SQLTagRepository(session)