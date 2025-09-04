from fastapi import Depends
from sqlmodel import Session

from app.src.infrastructure.db.session import get_session
from app.src.use_cases.tag.create_tag_use_case import CreateTagUseCase
from app.src.use_cases.tag.delete_tag_use_case import DeleteTagUseCase
from app.src.use_cases.tag.update_tag_use_case import UpdateTagUseCase
from app.src.use_cases.room.delete_room_use_case import DeleteRoomUseCase
from app.src.use_cases.room.update_room_use_case import UpdateRoomUseCase
from app.src.use_cases.tag.get_tag_list_use_case import GetTagListUseCase
from app.src.use_cases.room.create_room_use_case import CreateRoomUseCase
from app.src.use_cases.tag.get_tag_by_id_use_case import GetTagByIdUseCase
from app.src.use_cases.room.get_room_list_use_case import GetRoomListUseCase
from app.src.use_cases.room.get_room_by_id_use_case import GetRoomByIdUseCase
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.domain.interface_repositories.room_repository import RoomRepository
from app.src.infrastructure.db.repositories.tag_repository_sql import SQLTagRepository
from app.src.infrastructure.db.repositories.room_repository_sql import SQLRoomRepository

get_session_dep = Depends(get_session)


# Tag 

def tag_repository(session: Session = get_session_dep) -> TagRepository:
    return SQLTagRepository(session)


tag_repo_dep = Depends(tag_repository)


def get_tag_by_id_use_case(tag_repository: TagRepository = tag_repo_dep) -> GetTagByIdUseCase:
    return GetTagByIdUseCase(tag_repository)


def get_tag_list_use_case(tag_repository: TagRepository = tag_repo_dep) -> GetTagListUseCase:
    return GetTagListUseCase(tag_repository)


def create_tag_use_case(tag_repository: TagRepository = tag_repo_dep) -> CreateTagUseCase:
    return CreateTagUseCase(tag_repository)


def update_tag_use_case(tag_repository: TagRepository = tag_repo_dep) -> UpdateTagUseCase:
    return UpdateTagUseCase(tag_repository)


def delete_tag_use_case(tag_repository: TagRepository = tag_repo_dep) -> DeleteTagUseCase:
    return DeleteTagUseCase(tag_repository)



# Room

def room_repository(session: Session = get_session_dep) -> RoomRepository:
    return SQLRoomRepository(session)


room_repo_dep = Depends(room_repository)


def get_room_by_id_use_case(room_repository: RoomRepository = room_repo_dep) -> GetRoomByIdUseCase:
    return GetRoomByIdUseCase(room_repository)


def get_room_list_use_case(room_repository: RoomRepository = room_repo_dep) -> GetRoomListUseCase:
    return GetRoomListUseCase(room_repository)


def create_room_use_case(room_repository: RoomRepository = room_repo_dep) -> CreateRoomUseCase:
    return CreateRoomUseCase(room_repository)


def update_room_use_case(room_repository: RoomRepository = room_repo_dep) -> UpdateRoomUseCase:
    return UpdateRoomUseCase(room_repository)


def delete_room_use_case(room_repository: RoomRepository = room_repo_dep) -> DeleteRoomUseCase:
    return DeleteRoomUseCase(room_repository) 