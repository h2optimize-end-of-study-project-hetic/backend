import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.domain.entities.user_group import UserGroup
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.user_group.delete_user_group_use_case import DeleteUserGroupUseCase
from app.src.use_cases.user_group.update_user_group_use_case import UpdateUserGroupUseCase
from app.src.use_cases.user_group.create_user_group_use_case import CreateUserGroupUseCase
from app.src.use_cases.user_group.get_user_group_list_use_case import GetUserGroupListUseCase
from app.src.use_cases.user_group.get_user_group_by_id_use_case import GetUserGroupByIdUseCase
from app.src.presentation.api.common.generic_model import PaginationMetadataModel
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.presentation.api.user_group.user_group_model import (
    PaginatedListUserGroupModelResponse,
    UserGroupCreateModelRequest,
    UserGroupModelResponse,
    UserGroupUpdateModelRequest,
)
from app.src.presentation.dependencies import (
    create_user_group_use_case,
    delete_user_group_use_case,
    get_user_group_by_id_use_case,
    get_user_group_list_use_case,
    update_user_group_use_case,
)
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

user_group_not_found = OpenApiErrorResponseConfig(code=404, description="UserGroup not found", detail="UserGroup with ID '123' not found")
user_group_already_exist = OpenApiErrorResponseConfig(
    code=409, description="UserGroup already exists", detail="UserGroup with file_name 'Building A - Floor 1' already exists"
)
creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Failed to create UserGroup")
update_error = OpenApiErrorResponseConfig(code=406, description="Update fails", detail="Failed to update UserGroup")
deletion_error = OpenApiErrorResponseConfig(code=406, description="Deletion fails", detail="Failed to delete UserGroup")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")


logger = logging.getLogger(__name__)
user_group_router = APIRouter(
    prefix=f"/{OpenApiTags.user_group.value}", tags=[OpenApiTags.user_group]
)  # user_groups and OpenApiUserGroups are not bind to the entity user_group. It's just the param of APIRouter


@user_group_router.post(
    "",
    summary="Create a new user_group",
    response_model=UserGroupModelResponse,
    response_description="Details of the created user_group",
    responses=generate_responses([user_group_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_user_group(
    use_case: Annotated[CreateUserGroupUseCase, Depends(create_user_group_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    user_group: Annotated[UserGroupCreateModelRequest, Body(embed=True)],

):
    """
    Create a new user_group

    - **group_id** : The group ID to which this user_group is attached to
    - **user_id** : The user ID to which this user_group is attached to
    """
    try:
        user_group_entity = UserGroup(
            # id=None,
            group_id=user_group.group_id,
            user_id=user_group.user_id,
            created_at=None,
            updated_at=None,
        )

        new_user_group: UserGroup = use_case.execute(user_group_entity)

        return UserGroupModelResponse(**new_user_group.to_dict())

    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@user_group_router.get(
    "",
    summary="Retrieve a list of user_groups",
    response_model=PaginatedListUserGroupModelResponse,
    response_description="Detailed information of the requested user_groups",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_user_group_list(
    use_case: Annotated[GetUserGroupListUseCase, Depends(get_user_group_list_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int | None = Query(20, ge=1, description="Number of elements return"),
):
    """
    Retrieve a list of user_groups

    - **cursor**: Optional cursor for pagination (returns user_groups with id >= cursor)
    - **limit**: Number of user_groups to return (default: 20)
    """
    try:
        result = use_case.execute(cursor, limit)

        user_group_models = [UserGroupModelResponse(**user_group.to_dict()) for user_group in result.user_groups]

        metadata = PaginationMetadataModel(
            total=result.total,
            chunk_size=result.chunk_size,
            chunk_count=result.chunk_count,
            current_cursor=result.current_cursor,
            first_cursor=result.first_cursor,
            last_cursor=result.last_cursor,
            next_cursor=result.next_cursor,
        )

        response = PaginatedListUserGroupModelResponse(data=user_group_models, metadata=metadata)

        return response

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@user_group_router.get(
    "/{user_id}/{group_id}",
    summary="Retrieve user_group info by user_id and group_id",
    response_model=UserGroupModelResponse,
    response_description="Detailed information of the requested user_group",
    responses=generate_responses([user_group_not_found, unexpected_error]),
    deprecated=False,
)
async def read_user_group(
    use_case: Annotated[GetUserGroupByIdUseCase, Depends(get_user_group_by_id_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    user_id: int = Path(..., ge=1, description="The user ID (positive integer)"),
    group_id: int = Path(..., ge=1, description="The group ID (positive integer)")
):
    """
    Retrieve a user_group by its composite key (user_id, group_id)
    """
    try:
        user_group_entity: UserGroup = use_case.execute(user_id, group_id)

        return UserGroupModelResponse(**user_group_entity.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@user_group_router.patch(
    "/{user_id}/{group_id}",
    summary="Update a user_group partially",
    response_model=UserGroupModelResponse,
    responses=generate_responses([user_group_not_found, user_group_already_exist, unexpected_error]),
)
async def update_user_group(
    use_case: Annotated[UpdateUserGroupUseCase, Depends(update_user_group_use_case)],
    user_group: Annotated[UserGroupUpdateModelRequest, Body(embed=True)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    user_id: int = Path(..., ge=1, description="User ID of the user_group"),
    group_id: int = Path(..., ge=1, description="Group ID of the user_group"),
):
    try:
        update_data = user_group.model_dump(exclude_unset=True)
        updated_user_group = use_case.execute(user_id, group_id, update_data)

        return UserGroupModelResponse(**updated_user_group.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except UpdateFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@user_group_router.delete(
    "/{user_id}/{group_id}",
    summary="Delete a user_group by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses([user_group_not_found, deletion_error, unexpected_error]),
)
async def delete_user_group(
    use_case: Annotated[DeleteUserGroupUseCase, Depends(delete_user_group_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    user_id: int = Path(..., ge=1, description="User ID of the user_group"),
    group_id: int = Path(..., ge=1, description="Group ID of the user_group"),
):
    try:
        use_case.execute(user_id, group_id)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Failed to execute request on UserGroup"
        ) from e
    except DeletionFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
