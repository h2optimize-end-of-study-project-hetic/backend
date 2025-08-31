import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.domain.entities.group import Group
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.group.delete_group_use_case import DeleteGroupUseCase
from app.src.use_cases.group.update_group_use_case import UpdateGroupUseCase
from app.src.use_cases.group.create_group_use_case import CreateGroupUseCase
from app.src.use_cases.group.get_group_list_use_case import GetGroupListUseCase
from app.src.use_cases.group.get_group_by_id_use_case import GetGroupByIdUseCase
from app.src.presentation.api.common.generic_model import PaginationMetadataModel
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.presentation.api.group.group_model import (
    PaginatedListGroupModelResponse,
    GroupCreateModelRequest,
    GroupModelResponse,
    GroupUpdateModelRequest,
)
from app.src.presentation.dependencies import (
    create_group_use_case,
    delete_group_use_case,
    get_group_by_id_use_case,
    get_group_list_use_case,
    update_group_use_case,
)
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

group_not_found = OpenApiErrorResponseConfig(code=404, description="Group not found", detail="Group with ID '123' not found")
group_already_exist = OpenApiErrorResponseConfig(
    code=409, description="Group already exists", detail="Group with file_name 'Building A - Floor 1' already exists"
)
creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Failed to create Group")
update_error = OpenApiErrorResponseConfig(code=406, description="Update fails", detail="Failed to update Group")
deletion_error = OpenApiErrorResponseConfig(code=406, description="Deletion fails", detail="Failed to delete Group")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")


logger = logging.getLogger(__name__)
group_router = APIRouter(
    prefix=f"/{OpenApiTags.group.value}", tags=[OpenApiTags.group]
)  # groups and OpenApiGroups are not bind to the entity group. It's just the param of APIRouter


@group_router.post(
    "",
    summary="Create a new group",
    response_model=GroupModelResponse,
    response_description="Details of the created group",
    responses=generate_responses([group_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_group(
    use_case: Annotated[CreateGroupUseCase, Depends(create_group_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    group: Annotated[GroupCreateModelRequest, Body(embed=True)],

):
    """
    Create a new group

    - **name** : The name of the group
    - **description** : The purpose of the group
    - **member_count**: The number of people in the group

    """
    try:
        group_entity = Group(
            id=None,
            name=group.name,
            description=group.description,
            member_count=group.member_count,
            start_at=group.start_at,
            end_at=group.end_at,
            created_at=None,
            updated_at=None,
        )

        new_group: Group = use_case.execute(group_entity)

        return GroupModelResponse(**new_group.to_dict())

    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@group_router.get(
    "",
    summary="Retrieve a list of groups",
    response_model=PaginatedListGroupModelResponse,
    response_description="Detailed information of the requested groups",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_group_list(
    use_case: Annotated[GetGroupListUseCase, Depends(get_group_list_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int | None = Query(20, ge=1, description="Number of elements return"),
):
    """
    Retrieve a list of groups

    - **cursor**: Optional cursor for pagination (returns groups with id >= cursor)
    - **limit**: Number of groups to return (default: 20)
    """
    try:
        result = use_case.execute(cursor, limit)

        group_models = [GroupModelResponse(**group.to_dict()) for group in result.groups]

        metadata = PaginationMetadataModel(
            total=result.total,
            chunk_size=result.chunk_size,
            chunk_count=result.chunk_count,
            current_cursor=result.current_cursor,
            first_cursor=result.first_cursor,
            last_cursor=result.last_cursor,
            next_cursor=result.next_cursor,
        )

        response = PaginatedListGroupModelResponse(data=group_models, metadata=metadata)

        return response

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@group_router.get(
    "/{group_id}",
    summary="Retrieve group info by ID",
    response_model=GroupModelResponse,
    response_description="Detailed information of the requested group",
    responses=generate_responses([group_not_found, unexpected_error]),
    deprecated=False,
)
async def read_group(
    use_case: Annotated[GetGroupByIdUseCase, Depends(get_group_by_id_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    group_id: int = Path(..., ge=1, description="The group ID (positive integer)"),
):
    """
    Retrieve a group by its unique identifier

    - **group_id**: Must be a positive integer (≥ 1)
    """
    try:
        group_entity: Group = use_case.execute(group_id)

        return GroupModelResponse(**group_entity.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@group_router.patch(
    "/{group_id}",
    summary="Update a group partially",
    response_model=GroupModelResponse,
    responses=generate_responses([group_not_found, group_already_exist, unexpected_error]),
)
async def update_group(
    use_case: Annotated[UpdateGroupUseCase, Depends(update_group_use_case)],
    group: Annotated[GroupUpdateModelRequest, Body(embed=True)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    group_id: int = Path(..., ge=1, description="ID of the group to update"),
):
    try:
        update_data = group.model_dump(exclude_unset=True)
        updated_group = use_case.execute(group_id, update_data)

        return GroupModelResponse(**updated_group.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except UpdateFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@group_router.delete(
    "/{group_id}",
    summary="Delete a group by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses([group_not_found, deletion_error, unexpected_error]),
)
async def delete_group(
    use_case: Annotated[DeleteGroupUseCase, Depends(delete_group_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    group_id: int = Path(..., ge=1, description="ID of the group to delete"),
):
    try:
        use_case.execute(group_id)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Failed to execute request on Group"
        ) from e
    except DeletionFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
