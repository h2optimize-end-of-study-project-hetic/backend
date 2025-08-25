# app/src/use_cases/authentication/verify_user_use_case.py
from datetime import datetime, timedelta
import logging
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.src.common.exception import NotFoundError, VerifyUserError
from app.src.domain.entities.user import User
from app.src.domain.interface_repositories.user_repository import UserRepository
from app.src.presentation.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)


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
            raise NotFoundError("user", email)

        # Statut: actif et non supprimé
        if not user.is_active or user.is_delete:
            raise VerifyUserError("No access")

        # compare le mot de passe en clair au hash stocké dans user.password
        if not self._verify_password(password, user.password):
            raise VerifyUserError("Wrong credentials")

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
            test = pwd_context.verify(plain, hashed)
            logger.error("Résultat de la vérification :", test)
            # Si tu veux régénérer un hash du mot de passe en clair (optionnel, à ne pas faire en prod)
            logger.error("Nouveau hash :", pwd_context.hash(plain))
            return test
        except Exception:
            return False

    def _create_access_token(self, data: dict, minutes: int) -> str:
        to_encode = data.copy()
        to_encode["exp"] = datetime.now() + timedelta(minutes=minutes)
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
