from app.src.use_cases.authentication.get_current_user_use_case import GetCurrentUserUseCase
from app.src.use_cases.authentication.verify_user_use_case import VerifyUserUseCase
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, SQLModel
from typing import Type


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

from app.src.domain.interface_repositories.user_repository import UserRepository
from app.src.infrastructure.db.repositories.user_repository_sql import SQLUserRepository
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

from app.src.use_cases.building.create_building_use_case import CreateBuildingUseCase
from app.src.use_cases.building.delete_building_use_case import DeleteBuildingUseCase
from app.src.use_cases.building.update_building_use_case import UpdateBuildingUseCase
from app.src.use_cases.building.get_building_list_use_case import GetBuildingListUseCase
from app.src.use_cases.building.get_building_by_id_use_case import GetBuildingByIdUseCase
from app.src.domain.interface_repositories.building_repository import BuildingRepository
from app.src.infrastructure.db.repositories.building_repository_sql import SQLBuildingRepository

from app.src.use_cases.group.create_group_use_case import CreateGroupUseCase
from app.src.use_cases.group.delete_group_use_case import DeleteGroupUseCase
from app.src.use_cases.group.update_group_use_case import UpdateGroupUseCase
from app.src.use_cases.group.get_group_list_use_case import GetGroupListUseCase
from app.src.use_cases.group.get_group_by_id_use_case import GetGroupByIdUseCase
from app.src.domain.interface_repositories.group_repository import GroupRepository
from app.src.infrastructure.db.repositories.group_repository_sql import SQLGroupRepository

from app.src.use_cases.user_group.create_user_group_use_case import CreateUserGroupUseCase
from app.src.use_cases.user_group.delete_user_group_use_case import DeleteUserGroupUseCase
from app.src.use_cases.user_group.update_user_group_use_case import UpdateUserGroupUseCase
from app.src.use_cases.user_group.get_user_group_list_use_case import GetUserGroupListUseCase
from app.src.use_cases.user_group.get_user_group_by_id_use_case import GetUserGroupByIdUseCase
from app.src.domain.interface_repositories.user_group_repository import UserGroupRepository
from app.src.infrastructure.db.repositories.user_group_repository_sql import SQLUserGroupRepository

from app.src.infrastructure.db.session import get_session_recorded
from app.src.infrastructure.db.repositories.sensor_repository_sql import SQLSensorRepository
from app.src.infrastructure.db.models.sensor_model import (
    SensorButtonModel,
    SensorHumidityModel,
    SensorMotionModel,
    SensorNeighborsCountModel,
    SensorNeighborsDetailModel,
    SensorPressureModel,
    SensorTemperatureModel,
    SensorVoltageModel,
)

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


# building

def building_repository(session: Session = get_session_dep) -> BuildingRepository:
    return SQLBuildingRepository(session)

building_repo_dep = Depends(building_repository)

def get_building_by_id_use_case(building_repository: BuildingRepository = building_repo_dep) -> GetBuildingByIdUseCase:
    return GetBuildingByIdUseCase(building_repository)

def get_building_list_use_case(building_repository: BuildingRepository = building_repo_dep) -> GetBuildingListUseCase:
    return GetBuildingListUseCase(building_repository)

def create_building_use_case(building_repository: BuildingRepository = building_repo_dep) -> CreateBuildingUseCase:
    return CreateBuildingUseCase(building_repository)

def update_building_use_case(building_repository: BuildingRepository = building_repo_dep) -> UpdateBuildingUseCase:
    return UpdateBuildingUseCase(building_repository)

def delete_building_use_case(building_repository: BuildingRepository = building_repo_dep) -> DeleteBuildingUseCase:
    return DeleteBuildingUseCase(building_repository) 

# group

def group_repository(session: Session = get_session_dep) -> GroupRepository:
    return SQLGroupRepository(session)

group_repo_dep = Depends(group_repository)

def get_group_by_id_use_case(group_repository: GroupRepository = group_repo_dep) -> GetGroupByIdUseCase:
    return GetGroupByIdUseCase(group_repository)

def get_group_list_use_case(group_repository: GroupRepository = group_repo_dep) -> GetGroupListUseCase:
    return GetGroupListUseCase(group_repository)

def create_group_use_case(group_repository: GroupRepository = group_repo_dep) -> CreateGroupUseCase:
    return CreateGroupUseCase(group_repository)

def update_group_use_case(group_repository: GroupRepository = group_repo_dep) -> UpdateGroupUseCase:
    return UpdateGroupUseCase(group_repository)

def delete_group_use_case(group_repository: GroupRepository = group_repo_dep) -> DeleteGroupUseCase:
    return DeleteGroupUseCase(group_repository) 


# user_group

def user_group_repository(session: Session = get_session_dep) -> UserGroupRepository:
    return SQLUserGroupRepository(session)

user_group_repo_dep = Depends(user_group_repository)

def get_user_group_by_id_use_case(user_group_repository: UserGroupRepository = user_group_repo_dep) -> GetUserGroupByIdUseCase:
    return GetUserGroupByIdUseCase(user_group_repository)

def get_user_group_list_use_case(user_group_repository: UserGroupRepository = user_group_repo_dep) -> GetUserGroupListUseCase:
    return GetUserGroupListUseCase(user_group_repository)

def create_user_group_use_case(user_group_repository: UserGroupRepository = user_group_repo_dep) -> CreateUserGroupUseCase:
    return CreateUserGroupUseCase(user_group_repository)

def update_user_group_use_case(user_group_repository: UserGroupRepository = user_group_repo_dep) -> UpdateUserGroupUseCase:
    return UpdateUserGroupUseCase(user_group_repository)

def delete_user_group_use_case(user_group_repository: UserGroupRepository = user_group_repo_dep) -> DeleteUserGroupUseCase:
    return DeleteUserGroupUseCase(user_group_repository) 

# Sensor

SENSOR_MODEL_MAP: dict[str, tuple[Type[SQLModel], str]] = {
    # alias_url → (Model, colonne temporelle)
    "button": (SensorButtonModel, "time"),
    "humidity": (SensorHumidityModel, "time"),
    "motion": (SensorMotionModel, "time"),
    "neighbors_count": (SensorNeighborsCountModel, "time"),
    "neighbors_detail": (SensorNeighborsDetailModel, "time"),
    "pressure": (SensorPressureModel, "time"),
    "temperature": (SensorTemperatureModel, "time"),
    "voltage": (SensorVoltageModel, "time"),
    "sensor_button": (SensorButtonModel, "time"),
    "sensor_humidity": (SensorHumidityModel, "time"),
    "sensor_motion": (SensorMotionModel, "time"),
    "sensor_neighbors_count": (SensorNeighborsCountModel, "time"),
    "sensor_neighbors_detail": (SensorNeighborsDetailModel, "time"),
    "sensor_pressure": (SensorPressureModel, "time"),
    "sensor_temperature": (SensorTemperatureModel, "time"),
    "sensor_voltage": (SensorVoltageModel, "time"),
}


def get_sensor_repo(
    kind: str,
    session: Session = Depends(get_session_recorded),
) -> SQLSensorRepository:
    entry = SENSOR_MODEL_MAP.get(kind)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown sensor kind '{kind}'.",
        )

    model, ts_attr = entry
    return SQLSensorRepository(session, model, ts_attr)
