import logging
from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends

from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.presentation.core.config import settings
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.presentation.api.tool.tool_model import UserModelResponse
from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses


unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")

logger = logging.getLogger(__name__)

tool_router = APIRouter(prefix=f"/{OpenApiTags.tool.value}", tags=[OpenApiTags.tool])

@tool_router.get(
    "",
    summary="Retrieve a list of info",
    response_description="Detailed information of the application context",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_tag_list(
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))]
):
    """
    Retrieve a information on the app
    """
    return {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "env": settings.ENVIRONMENT,
        "log_level": settings.LOG_LEVEL,
        "debug": settings.is_debug,
    }


@tool_router.get("/public", summary="Public info")
async def public_route():
    return {"message": "This is a public route, no authentication required."}


@tool_router.get("/private", summary="Private info")
async def private_route(
    user: Annotated[User, Depends(secure_ressources())]
):
    result = UserModelResponse(**user.to_dict())
    return {
        "message": "This is a private route",
        "user": result
    }


@tool_router.get("/private/admin", summary="Admin info")
async def private_admin_route(
    user: Annotated[User, Depends(secure_ressources([Role.admin]))]
):
    result = UserModelResponse(**user.to_dict())
    return {
        "message":"This is an admin route",
        "user": result
    }


@tool_router.get("/private/interne", summary="interne info")
async def private_intern_route(
    user: Annotated[User, Depends(secure_ressources([Role.intern]))]
):
    result = UserModelResponse(**user.to_dict())
    return {
        "message": "This is an interne route",
        "user": result
    }


@tool_router.get("/private/internandguest", summary="interne info")
async def private_intern_and_guest_route(
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))]
):
    result = UserModelResponse(**user.to_dict())
    return {
        "message": "This is an interne route",
        "user": result
    }