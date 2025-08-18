from app.src.domain.interface_repositories.user_repository import UserRepository
from app.src.infrastructure.db.repositories.user_repository_sql import SQLUserRepository
from app.src.use_cases.authentication.get_current_user_use_case import GetCurrentUserUseCase
from app.src.use_cases.authentication.verify_user_use_case import VerifyUserUseCase
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

from app.src.use_cases.map.create_map_use_case import CreateMapUseCase
from app.src.use_cases.map.delete_map_use_case import DeleteMapUseCase
from app.src.use_cases.map.update_map_use_case import UpdateMapUseCase
from app.src.use_cases.map.get_map_list_use_case import GetMapListUseCase
from app.src.use_cases.map.get_map_by_id_use_case import GetMapByIdUseCase
from app.src.domain.interface_repositories.map_repository import MapRepository
from app.src.infrastructure.db.repositories.map_repository_sql import SQLMapRepository

from app.src.use_cases.user.create_user_use_case import CreateUserUseCase
from app.src.use_cases.user.delete_user_use_case import DeleteUserUseCase
from app.src.use_cases.user.update_user_use_case import UpdateUserUseCase
from app.src.use_cases.user.get_user_by_list_use_case import GetUserListUseCase
from app.src.use_cases.user.get_user_by_id_use_case import GetUserByIdUseCase
from app.src.domain.interface_repositories.user_repository import UserRepository
from app.src.infrastructure.db.repositories.user_repository_sql import SQLUserRepository

get_session_dep = Depends(get_session)


# Tag 

def tag_repository(session: Session = get_session_dep) -> TagRepository:
    return SQLTagRepository(session)

def user_repository(session: Session = get_session_dep) -> UserRepository:
    return SQLUserRepository(session)


tag_repo_dep = Depends(tag_repository)
user_repo_dep = Depends(user_repository)

def get_current_user_use_case(user_repository: UserRepository = user_repo_dep) -> GetCurrentUserUseCase:
    return GetCurrentUserUseCase(user_repository)

def get_verify_user_use_case(user_repository: UserRepository = user_repo_dep) -> VerifyUserUseCase:
    return VerifyUserUseCase(user_repository)

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



def map_repository(session: Session = get_session_dep) -> MapRepository:
    return SQLMapRepository(session)


map_repo_dep = Depends(map_repository)


def get_map_by_id_use_case(map_repository: MapRepository = map_repo_dep) -> GetMapByIdUseCase:
    return GetMapByIdUseCase(map_repository)


def get_map_list_use_case(map_repository: MapRepository = map_repo_dep) -> GetMapListUseCase:
    return GetMapListUseCase(map_repository)


def create_map_use_case(map_repository: MapRepository = map_repo_dep) -> CreateMapUseCase:
    return CreateMapUseCase(map_repository)


def update_map_use_case(map_repository: MapRepository = map_repo_dep) -> UpdateMapUseCase:
    return UpdateMapUseCase(map_repository)


def delete_map_use_case(map_repository: MapRepository = map_repo_dep) -> DeleteMapUseCase:
    return DeleteMapUseCase(map_repository)



def user_repository(session: Session = get_session_dep) -> UserRepository:
    return SQLUserRepository(session)


def user_repository(session: Session = get_session_dep) -> UserRepository:
    return SQLUserRepository(session)

user_repo_dep = Depends(user_repository)


def get_user_by_id_use_case(user_repository: UserRepository = user_repo_dep) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(user_repository)


def get_user_list_use_case(user_repository: UserRepository = user_repo_dep) -> GetUserListUseCase:
    return GetUserListUseCase(user_repository)


def create_user_use_case(user_repository: UserRepository = user_repo_dep) -> CreateUserUseCase:
    return CreateUserUseCase(user_repository)


def update_user_use_case(user_repository: UserRepository = user_repo_dep) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_repository)


def delete_user_use_case(user_repository: UserRepository = user_repo_dep) -> DeleteUserUseCase:
    return DeleteUserUseCase(user_repository)
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
