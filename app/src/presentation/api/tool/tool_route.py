import logging

from fastapi import APIRouter, HTTPException, Request, status

from app.src.domain.entities.role import Role
from app.src.presentation.core.config import settings
from app.src.presentation.core.open_api_tags import OpenApiTags
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
async def read_tag_list():
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



@tool_router.get(
    "/admin",
    summary="Retrieve a list of info",
    response_description="Detailed information of the application context",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def admin_tag_list(request: Request):
    """
    Return ok if user is authenticated and has role admin
    """
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    if user.get("role") != Role.admin.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    return {"ok": True, "user": user}
