from typing import Annotated
from app.src.presentation.dependencies import get_current_user_use_case
from app.src.use_cases.authentication.get_current_user_use_case import GetCurrentUserUseCase
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.src.presentation.core.config import settings
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
import logging
from app.src.presentation.api.authentication.authentication_model import User
from app.src.presentation.api.authentication.authentication_model import Token
from app.src.presentation.api.authentication.authentication_model import UserInDB

unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix=f"/{OpenApiTags.auth.value}", tags=[OpenApiTags.auth])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# @auth_router.post("/login", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email ou mot de passe incorrect"
#         )
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email, "role": user.role},
#         expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me",
    summary="Retrieve tag by ID",
    response_model=User,
    response_description="Detailed information of the requested tag"
    )
async def read_users_me(
    token: Annotated[str, Depends(oauth2_scheme)],
    use_case: Annotated[GetCurrentUserUseCase, Depends(get_current_user_use_case)]
):
    return use_case.execute(token)

