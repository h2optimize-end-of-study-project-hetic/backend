from typing import Any, List
from fastapi import APIRouter, HTTPException, Path

from app.domain.entities.tag import Tag
from app.services.http.core.open_api_tags import OpenApiTags
from app.services.http.api.tags.tags_model import PaginatedTagsModel, TagsModel

router = APIRouter(prefix="/tags", tags=[OpenApiTags.tags])


@router.get(
    "/",
    summary="Show tags",
    response_description="This is tags with the pagination",
    deprecated=False
)
async def read_tags(
    offset: int = 0, 
    limit: int = 100
) -> PaginatedTagsModel:
    """
    This will return all tags
    """

    all_tags = [
        TagsModel(id=1, name="Capteur 1", source_address="1126982881", description="Description 1"),
        TagsModel(id=2, name="Capteur 2", source_address="1041420528", description="Description 2"),
    ]

    paginated = all_tags[offset : offset + limit]

    return PaginatedTagsModel(
        data=paginated,
        count=len(all_tags),
        offset=offset,
        limit=limit
    )



def getTag (tag_id) : 
    if tag_id  ==0: 
        return Tag(id=1, name="Capteur 1", source_address="1126982881", description="Description 1")
    else :
        return


@router.get(
    "/{tag_id}",
    summary="Show tag",
    response_model=TagsModel,
    response_description="Details of the requested tag",
    responses={
        404: {
            "description": "Tag not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Tag not found"}
                }
            }
        }
    },
    deprecated=False
)
async def read_tag(
    tag_id: int = Path(..., ge=0, description="ID du tag, entier positif")
):
    """
    Get a tag by its ID.

    - **tag_id**: ID du tag doit être un entier positif
    """
    tag = getTag(tag_id)

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    return TagsModel(
        id=tag.id,
        name=tag.name,
        source_address=tag.source_address,
        description=tag.description
    )


