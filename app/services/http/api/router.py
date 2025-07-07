from fastapi import APIRouter

from app.services.http.api.tag.tag_route import router as tag_route

router = APIRouter()
router.include_router(tag_route)
