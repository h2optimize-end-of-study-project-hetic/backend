from fastapi import APIRouter, Path, Depends

from app.src.presentation.deps import get_user_repository
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.user.get_user_by_id import GetUserByIdUseCase
from app.src.domain.interface_repositories.user_repository import UserRepository
from app.src.presentation.api.user.users_model import UserModel

user_router = APIRouter(prefix="/users", tags=[OpenApiTags.users])

@user_router.get(
    "/{user_id}",
    summary="Show user",
    response_model=UserModel,
    response_description="Details of the requested user",
    responses={
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    },
    deprecated=False,
)
async def read_user(
    user_id: int = Path(..., ge=0, description="ID de l'utilisateur, entier positif"),
    repo: UserRepository = Depends(get_user_repository)
):
    """
    Get a user by its ID.

    - **user_id**: ID de l'utilisateur, doit être un entier positif
    """
    use_case = GetUserByIdUseCase(repo)
    return use_case.execute(user_id)