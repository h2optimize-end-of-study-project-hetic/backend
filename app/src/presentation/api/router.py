from fastapi import APIRouter
from app.src.presentation.api.tag.tag_route import tag_router
from app.src.presentation.api.map.map_route import map_router
from app.src.presentation.api.tool.tool_route import tool_router
from app.src.presentation.api.room.room_route import room_router
from app.src.presentation.api.user.users_route import user_router
from app.src.presentation.api.event.event_route import event_router
from app.src.presentation.api.group.group_route import group_router
from app.src.presentation.api.weather.weather_route import weather_router
from app.src.presentation.api.building.building_route import building_router
from app.src.presentation.api.room_tag.room_tag_route import room_tag_router
from app.src.presentation.api.event_room.event_room_route import event_room_router
from app.src.presentation.api.user_group.user_group_route import user_group_router
from app.src.presentation.api.authentication.authentication_route import auth_router
from app.src.presentation.api.sensor.sensor_route import sensor_router

router = APIRouter()
router.include_router(tag_router)
router.include_router(map_router)
router.include_router(room_router)
router.include_router(tool_router)
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(event_router)
router.include_router(group_router)
router.include_router(weather_router)
router.include_router(building_router)
router.include_router(room_tag_router)
router.include_router(event_room_router)
router.include_router(user_group_router)
router.include_router(sensor_router)
