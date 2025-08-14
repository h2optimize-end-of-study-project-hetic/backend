from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.src.presentation.core.config import settings
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
import logging

unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix=f"/{OpenApiTags.auth.value}", tags=[OpenApiTags.auth])


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    username: str
    lastname: str
    email: str
    role: str
    disabled: bool

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, email: str):
    if email in db:
        return UserInDB(**db[email])

def authenticate_user(email: str, password: str):
    user = get_user(settings.POSTGRES_DB, email)
    if not user:
        return None
    if user.disabled:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    user = get_user(settings.POSTGRES_DB, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return user

@auth_router.get("/api/health")
async def health():
    return {"status": "ok"}

@auth_router.post("/api/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ou mot de passe incorrect"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # On met l'email comme 'sub' et role
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/api/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
