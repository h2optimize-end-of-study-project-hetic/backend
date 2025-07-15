import logging
from typing import Annotated, List, Optional
from fastapi import Body, APIRouter, Path, Depends, HTTPException, Query, status

from app.src.domain.entities.tag import Tag
from app.src.use_cases.tag.create_tag import CreateTagUseCase
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.tag.get_tag_by_id import GetTagByIdUseCase
from app.src.use_cases.tag.get_tag_list import GetTagListUseCase
from app.src.presentation.api.tag.tags_model import PaginatedModel, PaginationMetadataModel, TagsModel, TagsCreateModel
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.common.exception import AlreadyExistsException, CreationFailedException, NotFoundException
from app.src.presentation.dependencies import get_tag_by_id_use_case, create_tag_use_case, get_tag_list_use_case

tag_not_found = OpenApiErrorResponseConfig(code=404, description="Tag not found", detail="Tag with ID '123' not found")
room_not_found = OpenApiErrorResponseConfig(code=404, description="Room not found", detail="Room with ID '14' not found")
tag_already_exist = OpenApiErrorResponseConfig(code=409, description="Tag already exists", detail="Tag with source_address '18458426' already exists")
creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Unable to create the tag")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")

logger = logging.getLogger(__name__)
tag_router = APIRouter(prefix="/tags", tags=[OpenApiTags.tags])

@tag_router.post(
    "",
    summary="Create a new tag",
    response_model=TagsModel,
    response_description="Details of the created tag",
    responses=generate_responses([tag_already_exist, creation_error, room_not_found, unexpected_error]),
    deprecated=False,
)
async def create_tag(
    use_case: Annotated[CreateTagUseCase, Depends(create_tag_use_case)],
    tag: Annotated[TagsCreateModel, Body(embed=True)],
):
    """
    Create a new tag

    - **name**: Name of the tag (minimum 3 characters, maximum 255 characters)
    - **description**: Optional description of the tag
    - **source_address**: Unique identifier for the tag source (minimum 3 characters)
    - **room_id**: Optional ID of the room associated with the tag, must be a positive integer (≥ 1)
    """
    try:
        tag_entity = Tag(
            id=None,
            name=tag.name,
            description=tag.description,
            source_address=tag.source_address,
            created_at=None,
            updated_at=None
        )

        new_tag:Tag = use_case.execute(tag_entity, tag.room_id)
            
        return TagsModel(**new_tag.to_dict())
    
    except NotFoundException as e:
        logger.debug(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    except CreationFailedException as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Unable to create the tag")
    
    except AlreadyExistsException  as e:
        logger.debug(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@tag_router.get(
    "",
    summary="Retrieve a list of tags",
    response_model=PaginatedModel,
    response_description="Detailed information of the requested tags",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_tag_list(
    use_case: Annotated[GetTagListUseCase, Depends(get_tag_list_use_case)], 
    cursor: Optional[str] = Query(None, description="Pagination cursor"),
    limit: Optional[int] = Query(20, ge=1, description="Number of elements return"),
):
    """
    Retrieve a list of tags

    - **cursor**: Optional cursor for pagination (returns tags with id >= cursor)
    - **limit**: Number of tags to return (default: 20)
    """
    try:
        result = use_case.execute(cursor, limit)

        tag_models = [TagsModel(**tag.to_dict()) for tag in result.tags]

        metadata = PaginationMetadataModel(
            total=result.total,
            chunk_size=result.chunk_size,
            chunk_count=result.chunk_count,
            current_cursor=result.current_cursor,
            first_cursor=result.first_cursor,
            last_cursor=result.last_cursor,
            next_cursor=result.next_cursor,
        )

        response = PaginatedModel(
            data=tag_models,
            metadata=metadata
        )

        return response
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@tag_router.get(
    "/{tag_id}",
    summary="Retrieve tag by ID",
    response_model=TagsModel,
    response_description="Detailed information of the requested tag",
    responses=generate_responses([tag_not_found, unexpected_error]),
    deprecated=False,
)
async def read_tag(
    use_case: Annotated[GetTagByIdUseCase, Depends(get_tag_by_id_use_case)], 
    tag_id: int = Path(..., ge=1, description="The tag ID (positive integer)"),
):
    """
    Retrieve a tag by its unique identifier

    - **tag_id**: Must be a positive integer (≥ 1)
    """
    try:
        tag_entity: Tag = use_case.execute(tag_id)

        return TagsModel(**tag_entity.to_dict())
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")