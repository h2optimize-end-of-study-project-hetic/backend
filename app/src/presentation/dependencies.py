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

from app.src.use_cases.event.create_event_use_case import CreateEventUseCase
from app.src.use_cases.event.delete_event_use_case import DeleteEventUseCase
from app.src.use_cases.event.update_event_use_case import UpdateEventUseCase
from app.src.use_cases.event.get_event_list_use_case import GetEventListUseCase
from app.src.use_cases.event.get_event_by_id_use_case import GetEventByIdUseCase
from app.src.domain.interface_repositories.event_repository import EventRepository
from app.src.infrastructure.db.repositories.event_repository_sql import SQLEventRepository
from app.src.domain.interface_repositories.user_repository import UserRepository
from app.src.infrastructure.db.repositories.user_repository_sql import SQLUserRepository

from app.src.use_cases.event_room.create_event_room_use_case import CreateEventRoomUseCase
from app.src.use_cases.event_room.delete_event_room_use_case import DeleteEventRoomUseCase
from app.src.use_cases.event_room.update_event_room_use_case import UpdateEventRoomUseCase
from app.src.use_cases.event_room.get_event_room_list_use_case import GetEventRoomListUseCase
from app.src.use_cases.event_room.get_event_room_by_id_use_case import GetEventRoomByIdUseCase
from app.src.domain.interface_repositories.event_room_repository import EventRoomRepository
from app.src.infrastructure.db.repositories.event_room_repository_sql import SQLEventRoomRepository

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

def event_repository(session: Session = get_session_dep) -> EventRepository:
    return SQLEventRepository(session)

event_repo_dep = Depends(event_repository)


def get_event_by_id_use_case(event_repository: EventRepository = event_repo_dep) -> GetEventByIdUseCase:
    return GetEventByIdUseCase(event_repository)


def get_event_list_use_case(event_repository: EventRepository = event_repo_dep) -> GetEventListUseCase:
    return GetEventListUseCase(event_repository)


def create_event_use_case(event_repository: EventRepository = event_repo_dep) -> CreateEventUseCase:
    return CreateEventUseCase(event_repository)


def update_event_use_case(event_repository: EventRepository = event_repo_dep) -> UpdateEventUseCase:
    return UpdateEventUseCase(event_repository)


def delete_event_use_case(event_repository: EventRepository = event_repo_dep) -> DeleteEventUseCase:
    return DeleteEventUseCase(event_repository)


# user

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


# event

def event_repository(session: Session = get_session_dep) -> EventRepository:
    return SQLEventRepository(session)

event_repo_dep = Depends(event_repository)


def get_event_by_id_use_case(event_repository: EventRepository = event_repo_dep) -> GetEventByIdUseCase:
    return GetEventByIdUseCase(event_repository)


def get_event_list_use_case(event_repository: EventRepository = event_repo_dep) -> GetEventListUseCase:
    return GetEventListUseCase(event_repository)


def create_event_use_case(event_repository: EventRepository = event_repo_dep) -> CreateEventUseCase:
    return CreateEventUseCase(event_repository)


def update_event_use_case(event_repository: EventRepository = event_repo_dep) -> UpdateEventUseCase:
    return UpdateEventUseCase(event_repository)


def delete_event_use_case(event_repository: EventRepository = event_repo_dep) -> DeleteEventUseCase:
    return DeleteEventUseCase(event_repository)



# event_room

def event_room_repository(session: Session = get_session_dep) -> EventRoomRepository:
    return SQLEventRoomRepository(session)


event_room_repo_dep = Depends(event_room_repository)


def get_event_room_by_id_use_case(event_room_repository: EventRoomRepository = event_room_repo_dep) -> GetEventRoomByIdUseCase:
    return GetEventRoomByIdUseCase(event_room_repository)


def get_event_room_list_use_case(event_room_repository: EventRoomRepository = event_room_repo_dep) -> GetEventRoomListUseCase:
    return GetEventRoomListUseCase(event_room_repository)


def create_event_room_use_case(event_room_repository: EventRoomRepository = event_room_repo_dep) -> CreateEventRoomUseCase:
    return CreateEventRoomUseCase(event_room_repository)


def update_event_room_use_case(event_room_repository: EventRoomRepository = event_room_repo_dep) -> UpdateEventRoomUseCase:
    return UpdateEventRoomUseCase(event_room_repository)


def delete_event_room_use_case(event_room_repository: EventRoomRepository = event_room_repo_dep) -> DeleteEventRoomUseCase:
    return DeleteEventRoomUseCase(event_room_repository) 
