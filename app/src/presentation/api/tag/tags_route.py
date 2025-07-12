from typing import Annotated
from fastapi import HTTPException
from fastapi import APIRouter, Path, Depends

from app.src.presentation.api.tag.tags_model import TagsModel
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.tag.get_tag_by_id import GetTagByIdUseCase
from app.src.presentation.dependencies import get_tag_by_id_use_case


tag_router = APIRouter(prefix="/tags", tags=[OpenApiTags.tags])

@tag_router.get(
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
    deprecated=False,
)
async def read_tag(
    use_case: Annotated[GetTagByIdUseCase, Depends(get_tag_by_id_use_case)], 
    tag_id: int = Path(..., ge=0, description="ID du tag, entier positif"),
):
    """
    Get a tag by its ID.

    - **tag_id**: ID du tag doit être un entier positif
    """
    try: 
        tag_entity = use_case.execute(tag_id)
        return TagsModel(**tag_entity.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Tag not found")
