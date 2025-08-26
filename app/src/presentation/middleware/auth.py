from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError, ExpiredSignatureError
from app.src.presentation.core.config import settings
from app.src.domain.entities.role import Role

async def jwt_middleware(request: Request, call_next):
    auth_header = request.headers.get("Authorization")
    request.state.user = None  # par défaut

    # Vérifie si la route commence par /tool/admin
    path = request.url.path
    is_admin_route = path.startswith("/api/v1/tool/admin")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            request.state.user = {
                "id": payload.get("sub"),
                "email": payload.get("email"),
                "role": payload.get("role")
            }

            # Vérifie le rôle admin si nécessaire
            if is_admin_route and request.state.user.get("role") != Role.admin.value:
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Not authorized"}
                )

        except ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token expired"})
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    elif is_admin_route:
        # Pas de token fourni pour une route admin
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

    response = await call_next(request)
    return response