from fastapi import Depends
from sqlmodel import Session

from app.src.infrastructure.db.session import get_session
from app.src.use_cases.tag.create_tag_use_case import CreateTagUseCase
from app.src.use_cases.tag.delete_tag_use_case import DeleteTagUseCase
from app.src.use_cases.tag.update_tag_use_case import UpdateTagUseCase
from app.src.use_cases.tag.get_tag_list_use_case import GetTagListUseCase
from app.src.use_cases.tag.get_tag_by_id_use_case import GetTagByIdUseCase
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.infrastructure.db.repositories.tag_repository_sql import SQLTagRepository

from app.src.use_cases.map.create_map_use_case import CreateMapUseCase
from app.src.use_cases.map.delete_map_use_case import DeleteMapUseCase
from app.src.use_cases.map.update_map_use_case import UpdateMapUseCase
from app.src.use_cases.map.get_map_list_use_case import GetMapListUseCase
from app.src.use_cases.map.get_map_by_id_use_case import GetMapByIdUseCase
from app.src.domain.interface_repositories.map_repository import MapRepository
from app.src.infrastructure.db.repositories.map_repository_sql import SQLMapRepository

get_session_dep = Depends(get_session)


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

