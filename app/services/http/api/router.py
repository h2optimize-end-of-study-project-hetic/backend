from fastapi import APIRouter

from app.services.http.api.tags.tags_route import router as tag_route

router = APIRouter()
router.include_router(tag_route)
