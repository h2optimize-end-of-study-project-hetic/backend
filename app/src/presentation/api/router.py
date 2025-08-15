from fastapi import APIRouter
from app.src.presentation.api.tag.tag_route import tag_router
from app.src.presentation.api.map.map_route import map_router
from app.src.presentation.api.tool.tool_route import tool_router
from app.src.presentation.api.user.users_route import user_router
from app.src.presentation.api.room.room_route import room_router
from app.src.presentation.api.authentication.authentication_route import auth_router

router = APIRouter()
router.include_router(tag_router)
router.include_router(map_router)
router.include_router(room_router)
router.include_router(tool_router)
router.include_router(user_router)
router.include_router(auth_router)
