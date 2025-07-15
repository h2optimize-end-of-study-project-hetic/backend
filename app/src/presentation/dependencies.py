from fastapi import Depends
from sqlmodel import Session

from app.src.infrastructure.db.session import get_session
from app.src.use_cases.tag.create_tag import CreateTagUseCase
from app.src.use_cases.tag.get_tag_by_id import GetTagByIdUseCase
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.domain.interface_repositories.room_repository import RoomRepository
from app.src.infrastructure.db.repositories.tag_repository_sql import SQLTagRepository
from app.src.infrastructure.db.repositories.room_repository_sql import SQLRoomRepository
from app.src.use_cases.tag.get_tag_list import GetTagListUseCase

def tag_repository(session: Session = Depends(get_session)) -> TagRepository:
    return SQLTagRepository(session)

def room_repository(session: Session = Depends(get_session)) -> RoomRepository:
    return SQLRoomRepository(session)

def get_tag_by_id_use_case(
    tag_repository: TagRepository = Depends(tag_repository)
) -> GetTagByIdUseCase:
    return GetTagByIdUseCase(tag_repository)

def get_tag_list_use_case(
    tag_repository: TagRepository = Depends(tag_repository)
) -> GetTagListUseCase:
    return GetTagListUseCase(tag_repository)

def create_tag_use_case(
    tag_repository: TagRepository = Depends(tag_repository),
    room_repository: RoomRepository = Depends(room_repository)
) -> CreateTagUseCase:
    return CreateTagUseCase(tag_repository, room_repository)

