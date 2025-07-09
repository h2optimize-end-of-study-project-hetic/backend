from fastapi import APIRouter, Path, Depends

from app.src.presentation.deps import get_tag_repository
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.tag.get_tag_by_id import GetTagByIdUseCase
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.presentation.api.tag.tags_model import TagsModel


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
    tag_id : int = Path(..., ge=0, description="ID du tag, entier positif"),
    repo : TagRepository = Depends(get_tag_repository)
):
    """
    Get a tag by its ID.

    - **tag_id**: ID du tag doit être un entier positif
    """
    use_case = GetTagByIdUseCase(repo)
    return use_case.execute(tag_id)
