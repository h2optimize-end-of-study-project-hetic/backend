import logging
from typing import Annotated

from app.src.presentation.api.authentication.authentication_model import UserModelResponse
from app.src.use_cases.view.get_user_in_group_by_group_id_use_case import GetUsersInGroupUseCase
from app.src.use_cases.view.get_planning_by_user_id_use_case import GetEventsForUserUseCase
from app.src.presentation.api.view.view_model import UserEventViewResponse
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.domain.entities.group import Group
from app.src.presentation.core.open_api_tags import OpenApiTags

from app.src.use_cases.view.get_user_in_group_by_group_id_use_case import GetUsersInGroupUseCase
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses

from app.src.presentation.dependencies import (
    get_user_events_use_case,
    get_users_in_group_use_case
)
from app.src.common.exception import (
    NotFoundError,
)

group_not_found = OpenApiErrorResponseConfig(code=404, description="View not found", detail="View with ID '123' not found")
group_already_exist = OpenApiErrorResponseConfig(
    code=409, description="View already exists", detail="View with ID '123' not found"
)
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")


logger = logging.getLogger(__name__)
view_router = APIRouter(
    prefix=f"/{OpenApiTags.view.value}", tags=[OpenApiTags.view]
)

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
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
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
    

@view_router.get("/users/{user_id}/events", response_model=list[UserEventViewResponse])

def get_user_events(
    user_id: int,
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    use_case: Annotated[GetEventsForUserUseCase, Depends(get_user_events_use_case)]
):
    try:
        results = use_case.execute(user_id)
        return [UserEventViewResponse(**dict(row)) for row in results]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
