import logging
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from app.src.domain.entities.user import User
from app.src.common.exception import NotFoundError
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.presentation.dependencies import get_verify_user_use_case
from app.src.presentation.api.tool.tool_model import UserModelResponse
from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig
from app.src.presentation.api.authentication.authentication_model import Token
from app.src.use_cases.authentication.verify_user_use_case import VerifyUserError, VerifyUserUseCase


unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix=f"/{OpenApiTags.auth.value}", tags=[OpenApiTags.auth])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auth_router.post("/login", response_model=Token)
async def login(
    use_case: Annotated[VerifyUserUseCase, Depends(get_verify_user_use_case)],
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Authenticates a user via email and password.
    Returns an access_token (JWT).
    """

    try:
        result = use_case.execute(email=form_data.username, password=form_data.password)
        return {"access_token": result["access_token"], "token_type": "bearer"}
    
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail="User not found") from e
    
    except VerifyUserError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e), headers={"WWW-Authenticate": "Bearer"}) from e
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@auth_router.get("/me",
    summary="Retrieve tag by ID",
    response_model=UserModelResponse,
    response_description="Detailed information of the requested tag"
)
async def read_users_me(
    user: Annotated[User, Depends(secure_ressources())]
):
    """
    Returns the authenticated user's information
    from the JWT token.
    """
    try:
        result = UserModelResponse(**user.to_dict())
        return result

    except NotFoundError as e :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"}) from e

    except Exception as e:
        logger.exception("Unexpected error while decoding token")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail="Internal server error") from e

