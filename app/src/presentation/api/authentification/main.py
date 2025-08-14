# app/src/presentation/api/authentification/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY manquante. Vérifie .env/.env.local et le dossier de lancement uvicorn.")

fake_db = {
    "john.doe@example.com": {
        "id": 1,
        "username": "John",
        "lastname": "Doe",
        "email": "john.doe@example.com",
        "hashed_password": "$2b$12$EcVC8zHJVGwhTX/qa1Ttq.Hk/m2bchwCF6hKPfS5IAyEuIJa6S78K",  # password123
        "role": "admin",
        "disabled": False,
    }
}

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

app = FastAPI()

# CORS (autorise le front Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, email: str):
    if email in db:
        return UserInDB(**db[email])

def authenticate_user(email: str, password: str):
    user = get_user(fake_db, email)
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
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    user = get_user(fake_db, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return user

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ou mot de passe incorrect"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # On met l'email comme 'sub' et role
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
