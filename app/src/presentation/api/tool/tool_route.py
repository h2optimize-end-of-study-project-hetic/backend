import logging

from fastapi import APIRouter

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
