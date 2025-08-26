from fastapi import APIRouter

from app.src.presentation.api.tag.tag_route import tag_router
from app.src.presentation.api.map.map_route import map_router
from app.src.presentation.api.tool.tool_route import tool_router
from app.src.presentation.api.user.users_route import user_router

router = APIRouter()
router.include_router(tag_router)
router.include_router(map_router)
router.include_router(tool_router)
router.include_router(user_router)
