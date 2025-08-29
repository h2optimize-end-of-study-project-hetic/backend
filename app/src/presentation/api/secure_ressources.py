from typing import Annotated
from jose import JWTError, jwt
from collections.abc import Sequence
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.common.exception import NotFoundError
from app.src.presentation.core.config import settings
from app.src.presentation.dependencies import get_current_user_use_case
from app.src.use_cases.authentication.get_current_user_use_case import GetCurrentUserUseCase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    use_case: Annotated[GetCurrentUserUseCase, Depends(get_current_user_use_case)] = None
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str = payload.get("sub")

        if not user_id_str:
            raise NotFoundError("user", token)
        
        user_id = int(user_id_str)

    except (JWTError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    try:
        user = use_case.execute(user_id)
        
        if not user or not user.is_active:
            raise NotFoundError("user", token)
            
        return user
        
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def check_user_permissions(user: User, required_roles: Sequence[Role] | None = None) -> None:
    if not required_roles:
        return
    
    if user.role == Role.admin.value:
        return
    
    required_role_values = []
    for role in required_roles:
        if isinstance(role, Role):
            required_role_values.append(role.value)
        elif isinstance(role, str):
            required_role_values.append(role)
        else:
            required_role_values.append(getattr(role, 'value', str(role)))
    
    if user.role not in required_role_values:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )


def require_roles(required_roles: Sequence[Role] | None = None):
    def dependency(user: User = Depends(get_current_user_from_token)) -> User:
        check_user_permissions(user, required_roles)
        return user
    
    return dependency


def secure_ressources(required_roles: Sequence[Role] | None = None):
    return require_roles(required_roles)