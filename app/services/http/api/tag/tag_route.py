from typing import Any, List
from fastapi import APIRouter, HTTPException
from app.domain.entities.tag import Tag
from app.services.http.api.tag.tag_model import PaginatedTags
from .tag_model import Tags

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/", response_model=PaginatedTags)
async def read_tags(offset: int = 0, limit: int = 100):
    
    all_tags = [
        Tags(id=1, name="Capteur 1", source_address="1126982881", description="Description 1"),
        Tags(id=2, name="Capteur 2", source_address="1041420528", description="Description 2"),
    ]

    paginated = all_tags[offset : offset + limit]

    return PaginatedTags(
        data=paginated,
        count=len(all_tags),
        offset=offset,
        limit=limit
    )
