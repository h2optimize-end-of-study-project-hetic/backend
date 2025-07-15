from fastapi import APIRouter

from app.src.presentation.api.tag.tags_route import tag_router

router = APIRouter()
router.include_router(tag_router)
