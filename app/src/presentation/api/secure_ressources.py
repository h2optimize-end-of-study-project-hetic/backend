from typing import Annotated
from collections.abc import Sequence
from jose import JWTError, jwt
from collections.abc import Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.common.exception import NotFoundError
from app.src.presentation.core.config import settings
from app.src.presentation.dependencies import get_current_user_use_case
from app.src.use_cases.authentication.get_current_user_use_case import GetCurrentUserUseCase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def secure_ressources(required_roles: Sequence[Role] | None = None) -> Callable:
    """
    Factory qui retourne une dépendance sécurisée :
      - Vérifie le token JWT
      - Récupère l'utilisateur
      - Vérifie optionnellement le rôle
    """

    async def dependency(
        token: str = Depends(oauth2_scheme),
        use_case: Annotated[GetCurrentUserUseCase, Depends(get_current_user_use_case)] = None
    ) -> User:
        try:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                user_id_str = payload.get("sub")

                if not user_id_str:
                    raise NotFoundError("user", token)
                
                user_id = int(user_id_str)

            except (JWTError, ValueError) as e:
                raise NotFoundError("user", token) from e

            user = use_case.execute(user_id)

            if not user or not user.is_active:
                raise NotFoundError("user", token)

            if required_roles and user.role != Role.admin.value and user.role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )

            return user

        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e

    return dependency
