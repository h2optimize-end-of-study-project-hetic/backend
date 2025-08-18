# app/src/use_cases/authentication/verify_user_use_case.py
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.src.common.exception import NotFoundError
from app.src.domain.entities.user import User
from app.src.domain.interface_repositories.user_repository import UserRepository
from app.src.presentation.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class VerifyUserError(Exception):
    """401/403 générique si email/mdp invalide ou compte désactivé/supprimé."""


class VerifyUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> dict:
        """
        - Récupère l'utilisateur par email
        - Vérifie mdp (bcrypt) + statut
        - Génère le token et retourne { access_token, token_type, user }
        """
        user: Optional[User] = self.user_repository.select_user_by_email(email)
        if user is None:
            # 404 cohérent avec ton NotFoundError (tu peux choisir 401 si tu préfères être moins verbeux)
            raise NotFoundError("user", email)

        # Statut: actif et non supprimé
        if not user.is_active or user.is_delete:
            raise VerifyUserError("Utilisateur désactivé ou supprimé")

        # compare le mot de passe en clair au hash stocké dans user.password
        if not self._verify_password(password, user.password):
            # 401
            raise VerifyUserError("Email ou mot de passe incorrect")

        token = self._create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                # si Role est un Enum, encoder la valeur; sinon, user.role est ok
                "role": getattr(user.role, "value", user.role),
            },
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }

    # --- helpers privés ---

    def _verify_password(self, plain: str, hashed: str) -> bool:
        try:
            return pwd_context.verify(plain, hashed)
        except Exception:
            return False

    def _create_access_token(self, data: dict, minutes: int) -> str:
        to_encode = data.copy()
        to_encode["exp"] = datetime.utcnow() + timedelta(minutes=minutes)
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
