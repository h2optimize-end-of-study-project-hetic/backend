from fastapi import APIRouter, Depends

from fastapi import APIRouter, HTTPException, Path

from app.src.domain.entities.tag import Tag
from app.src.presentation.deps import get_tag_repository
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.tag.get_tag_by_id import GetTagByIdUseCase
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.presentation.api.tag.tags_model import PaginatedTagsModel, TagsModel



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




# from typing import Any, List
# from fastapi import APIRouter, HTTPException, Path

# from app.src.domain.entities.tag import Tag
# from app.src.presentation.core.open_api_tags import OpenApiTags
# from app.src.presentation.api.tag.tags_model import PaginatedTagsModel, TagsModel


# router = APIRouter(prefix="/tags", tags=[OpenApiTags.tags])


# @router.get(
#     "/",
#     summary="Show tags",
#     response_description="This is tags with the pagination",
#     deprecated=False
# )
# async def read_tags(
#     offset: int = 0, 
#     limit: int = 100
# ) -> PaginatedTagsModel:
#     """
#     This will return all tags
#     """

#     all_tags = [
#         TagsModel(id=1, name="Capteur 1", source_address="1126982881", description="Description 1"),
#         TagsModel(id=2, name="Capteur 2", source_address="1041420528", description="Description 2"),
#     ]

#     paginated = all_tags[offset : offset + limit]

#     return PaginatedTagsModel(
#         data=paginated,
#         count=len(all_tags),
#         offset=offset,
#         limit=limit
#     )



# def getTag (tag_id) : 
#     if tag_id  ==0: 
#         return Tag(id=1, name="Capteur 1", source_address="1126982881", description="Description 1")
#     else :
#         return


# @router.get(
#     "/{tag_id}",
#     summary="Show tag",
#     response_model=TagsModel,
#     response_description="Details of the requested tag",
#     responses={
#         404: {
#             "description": "Tag not found",
#             "content": {
#                 "application/json": {
#                     "example": {"detail": "Tag not found"}
#                 }
#             }
#         }
#     },
#     deprecated=False
# )
# async def read_tag(
#     tag_id: int = Path(..., ge=0, description="ID du tag, entier positif")
# ):
#     """
#     Get a tag by its ID.

#     - **tag_id**: ID du tag doit être un entier positif
#     """
#     tag = getTag(tag_id)

#     if not tag:
#         raise HTTPException(status_code=404, detail="Tag not found")

#     return TagsModel(
#         id=tag.id,
#         name=tag.name,
#         source_address=tag.source_address,
#         description=tag.description
#     )






