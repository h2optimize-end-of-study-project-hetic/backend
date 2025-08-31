import logging
from typing import Annotated

from app.src.presentation.api.authentication.authentication_model import UserModelResponse
from app.src.use_cases.view.get_user_in_group_by_group_id_use_case import GetUsersInGroupUseCase
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.domain.entities.group import Group
from app.src.presentation.core.open_api_tags import OpenApiTags

from app.src.use_cases.view.get_user_in_group_by_group_id_use_case import GetUsersInGroupUseCase
from app.src.use_cases.group.get_group_by_id_use_case import GetGroupByIdUseCase
from app.src.presentation.api.common.generic_model import PaginationMetadataModel
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.presentation.api.group.group_model import (
    PaginatedListGroupModelResponse,
    GroupModelResponse,

)
from app.src.presentation.dependencies import (
    get_users_in_group_use_case
)
from app.src.common.exception import (
    NotFoundError,
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
view_router = APIRouter(
    prefix=f"/{OpenApiTags.view.value}", tags=[OpenApiTags.view]
)


# @view_router.get(
#     "/building_rooms",
#     summary="Retrieve a list of buildings and their rooms",
#     response_model=PaginatedListGroupModelResponse,
#     response_description="Detailed information of the requested",
#     responses=generate_responses([unexpected_error]),
#     deprecated=False,
# )
# async def read_building_rooms_list(
#     use_case: Annotated[GetGroupListUseCase, Depends(get_group_list_use_case)],
#     user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
#     cursor: str | None = Query(None, description="Pagination cursor"),
#     limit: int | None = Query(20, ge=1, description="Number of elements return"),
# ):
#     """
#     Retrieve a list of groups

#     - **cursor**: Optional cursor for pagination (returns groups with id >= cursor)
#     - **limit**: Number of groups to return (default: 20)
#     """
#     try:
#         result = use_case.execute(cursor, limit)

#         group_models = [GroupModelResponse(**group.to_dict()) for group in result.groups]

#         metadata = PaginationMetadataModel(
#             total=result.total,
#             chunk_size=result.chunk_size,
#             chunk_count=result.chunk_count,
#             current_cursor=result.current_cursor,
#             first_cursor=result.first_cursor,
#             last_cursor=result.last_cursor,
#             next_cursor=result.next_cursor,
#         )

#         response = PaginatedListGroupModelResponse(data=group_models, metadata=metadata)

#         return response

#     except Exception as e:
#         logger.error(f"Unexpected error: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


# @view_router.get(
#     "/building_rooms/{building_id}",
#     summary="Retrieve rooms of a building",
#     response_model=GroupModelResponse,
#     response_description="Detailed information of the requested building",
#     responses=generate_responses([group_not_found, unexpected_error]),
#     deprecated=False,
# )
# async def read_group(
#     use_case: Annotated[GetGroupByIdUseCase, Depends(get_group_by_id_use_case)],
#     user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
#     building_id: int = Path(..., ge=1, description="The group ID (positive integer)"),
# ):
#     """
#     Retrieve a group by its unique identifier

#     - **group_id**: Must be a positive integer (≥ 1)
#     """
#     try:
#         group_entity: Group = use_case.execute(building_id)

#         return GroupModelResponse(**group_entity.to_dict())

#     except NotFoundError as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
#     except Exception as e:
#         logger.error(f"Unexpected error: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@view_router.get(
    "/{group_id}/users",
    summary="Retrieve users from group ID",
    response_model=list[UserModelResponse],
    response_description="Detailed information of the requested group_id user",
    responses=generate_responses([group_not_found, unexpected_error]),
    deprecated=False,
)
async def get_group_users(
    group_id: int,
    # user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    use_case: Annotated[GetUsersInGroupUseCase, Depends(get_users_in_group_use_case)]
):
    try:
        users = use_case.execute(group_id)
        return [UserModelResponse(**user.model_dump()) for user in users]

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e