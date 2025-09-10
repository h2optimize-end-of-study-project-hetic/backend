import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from app.src.domain.entities.role import Role
from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.presentation.api.user.users_model import (
    UserBaseModelResponse,
    UserCreateModelNoAuth,
    UserModel,
    UserCreateModel,
    UserUpdateModel,
    PaginatedUsersModel,
)
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.domain.entities.user import User
from app.src.use_cases.user.create_user_use_case import CreateUserUseCase
from app.src.use_cases.user.get_user_by_id_use_case import GetUserByIdUseCase
from app.src.use_cases.user.get_user_by_list_use_case import GetUserListUseCase
from app.src.use_cases.user.update_user_use_case import UpdateUserUseCase
from app.src.use_cases.user.delete_user_use_case import DeleteUserUseCase
from app.src.presentation.dependencies import (
    create_user_use_case,
    get_user_by_id_use_case,
    get_user_list_use_case,
    update_user_use_case,
    delete_user_use_case,
)
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    NotFoundError,
    UpdateFailedError,
    ForeignKeyConstraintError,
)

user_not_found = OpenApiErrorResponseConfig(code=404, description="User not found", detail="User with this ID was not found")
user_already_exist = OpenApiErrorResponseConfig(code=409, description="User already exists", detail="User with this email already exists")
creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Failed to create User")
update_error = OpenApiErrorResponseConfig(code=406, description="Update fails", detail="Failed to update User")
deletion_error = OpenApiErrorResponseConfig(code=406, description="Deletion fails", detail="Failed to delete User")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")

logger = logging.getLogger(__name__)
user_router = APIRouter(prefix="/users", tags=[OpenApiTags.user])


@user_router.post(
    "/new",
    summary="Create a new user ",
    response_model=UserModel,
    response_description="Details of the created user",
    responses=generate_responses([user_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_user_no_auth(
    use_case: Annotated[CreateUserUseCase, Depends(create_user_use_case)],
    user_data: UserCreateModelNoAuth
):
    """
    Create a new user.
    """
    try:
        user_data.is_active = False
        user_data.role = Role.guest.value
        user_entity = User.from_dict(user_data.model_dump())
        new_user: User = use_case.execute(user_entity)
        return UserModel(**new_user.to_dict())
    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@user_router.post(
    "",
    summary="Create a new user",
    response_model=UserModel,
    response_description="Details of the created user",
    responses=generate_responses([user_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_user(
    use_case: Annotated[CreateUserUseCase, Depends(create_user_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    user_data: UserCreateModel
):
    """
    Create a new user.
    """
    try:  
        user_entity = User.from_dict(user_data.model_dump())
        new_user: User = use_case.execute(user_entity)
        return UserModel(**new_user.to_dict())
    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e

@user_router.get(
    "",
    summary="Retrieve a list of users",
    response_model=PaginatedUsersModel,
    response_description="Detailed information of the requested users",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_user_list(
    use_case: Annotated[GetUserListUseCase, Depends(get_user_list_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int | None = Query(20, ge=1, description="Number of elements to return"),
):
    """
    Retrieve a list of users.
    """
    try:
        result = use_case.execute(cursor, limit)
        user_models = [UserBaseModelResponse(**user.to_dict()) for user in result.users]
        return PaginatedUsersModel(
            data=user_models,
            count=result.total,
            offset=0,
            limit=limit
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@user_router.get(
    "/{user_id}",
    summary="Retrieve user info by ID",
    response_model=UserModel,
    response_description="Detailed information of the requested user",
    responses=generate_responses([user_not_found, unexpected_error]),
    deprecated=False,
)
async def read_user(
    use_case: Annotated[GetUserByIdUseCase, Depends(get_user_by_id_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    user_id: int = Path(..., ge=1, description="The user ID (positive integer)"),
):
    """
    Retrieve a user by its unique identifier.
    """
    try:
        user_entity: User = use_case.execute(user_id)
        if user_entity is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserModel(**user_entity.to_dict())
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e

@user_router.patch(
    "/{user_id}",
    summary="Update a user partially",
    response_model=UserModel,
    responses=generate_responses([user_not_found, user_already_exist, update_error, unexpected_error]),
)
async def update_user(
    use_case: Annotated[UpdateUserUseCase, Depends(update_user_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    user_id: int = Path(..., ge=1, description="ID of the user to update"),
    user_data: UserUpdateModel = None,
):
    try:
        if user_data is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided for update")
        updated_user = use_case.execute(user_id, user_data.dict(exclude_unset=True))
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserModel(**updated_user.to_dict())
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except UpdateFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e

@user_router.delete(
    "/{user_id}",
    summary="Delete a user by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses([user_not_found, deletion_error, unexpected_error]),
)
async def delete_user(
    use_case: Annotated[DeleteUserUseCase, Depends(delete_user_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    user_id: int = Path(..., ge=1, description="ID of the user to delete"),
):
    try:
        use_case.execute(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=str(e)
        ) from e
    except DeletionFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e