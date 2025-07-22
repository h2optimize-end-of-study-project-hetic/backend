import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.src.domain.entities.tag import Tag
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.tag.delete_tag_use_case import DeleteTagUseCase
from app.src.use_cases.tag.update_tag_use_case import UpdateTagUseCase
from app.src.use_cases.tag.create_tag_use_case import CreateTagUseCase
from app.src.use_cases.tag.get_tag_list_use_case import GetTagListUseCase
from app.src.use_cases.tag.get_tag_by_id_use_case import GetTagByIdUseCase
from app.src.presentation.api.common.generic_model import PaginationMetadataModel
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.presentation.api.tag.tag_model import (
    PaginatedListTagModelResponse,
    TagCreateModelRequest,
    TagModelResponse,
    TagUpdateModelRequest,
)
from app.src.presentation.dependencies import (
    create_tag_use_case,
    delete_tag_use_case,
    get_tag_by_id_use_case,
    get_tag_list_use_case,
    update_tag_use_case,
)
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

tag_not_found = OpenApiErrorResponseConfig(code=404, description="Tag not found", detail="Tag with ID '123' not found")
tag_already_exist = OpenApiErrorResponseConfig(
    code=409, description="Tag already exists", detail="Tag with source_address '18458426' already exists"
)
creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Failed to create Tag")
update_error = OpenApiErrorResponseConfig(code=406, description="Update fails", detail="Failed to upadte Tag")
deletion_error = OpenApiErrorResponseConfig(code=406, description="Deletion fails", detail="Failed to delete Tag")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")


logger = logging.getLogger(__name__)
tag_router = APIRouter(
    prefix=f"/{OpenApiTags.tag.value}", tags=[OpenApiTags.tag]
)  # tags and OpenApiTags are not bind to the entity tag. It's just the param of APIRouter


@tag_router.post(
    "",
    summary="Create a new tag",
    response_model=TagModelResponse,
    response_description="Details of the created tag",
    responses=generate_responses([tag_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_tag(
    use_case: Annotated[CreateTagUseCase, Depends(create_tag_use_case)],
    tag: Annotated[TagCreateModelRequest, Body(embed=True)],
):
    """
    Create a new tag

    - **name**: Name of the tag (minimum 3 characters, maximum 255 characters)
    - **description**: Optional description of the tag
    - **source_address**: Unique identifier for the tag source (minimum 3 characters)
    """
    try:
        tag_entity = Tag(
            id=None,
            name=tag.name,
            description=tag.description,
            source_address=tag.source_address,
            created_at=None,
            updated_at=None,
        )

        new_tag: Tag = use_case.execute(tag_entity)

        return TagModelResponse(**new_tag.to_dict())

    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@tag_router.get(
    "",
    summary="Retrieve a list of tags",
    response_model=PaginatedListTagModelResponse,
    response_description="Detailed information of the requested tags",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_tag_list(
    use_case: Annotated[GetTagListUseCase, Depends(get_tag_list_use_case)],
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int | None = Query(20, ge=1, description="Number of elements return"),
):
    """
    Retrieve a list of tags

    - **cursor**: Optional cursor for pagination (returns tags with id >= cursor)
    - **limit**: Number of tags to return (default: 20)
    """
    try:
        result = use_case.execute(cursor, limit)

        tag_models = [TagModelResponse(**tag.to_dict()) for tag in result.tags]

        metadata = PaginationMetadataModel(
            total=result.total,
            chunk_size=result.chunk_size,
            chunk_count=result.chunk_count,
            current_cursor=result.current_cursor,
            first_cursor=result.first_cursor,
            last_cursor=result.last_cursor,
            next_cursor=result.next_cursor,
        )

        response = PaginatedListTagModelResponse(data=tag_models, metadata=metadata)

        return response

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@tag_router.get(
    "/{tag_id}",
    summary="Retrieve tag by ID",
    response_model=TagModelResponse,
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

        return TagModelResponse(**tag_entity.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@tag_router.patch(
    "/{tag_id}",
    summary="Update a tag partially",
    response_model=TagModelResponse,
    responses=generate_responses([tag_not_found, tag_already_exist, unexpected_error]),
)
async def update_tag(
    use_case: Annotated[UpdateTagUseCase, Depends(update_tag_use_case)],
    tag: Annotated[TagUpdateModelRequest, Body(embed=True)],
    tag_id: int = Path(..., ge=1, description="ID of the tag to update"),
):
    try:
        update_data = tag.model_dump(exclude_unset=True)
        updated_tag = use_case.execute(tag_id, update_data)

        return TagModelResponse(**updated_tag.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except UpdateFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@tag_router.delete(
    "/{tag_id}",
    summary="Delete a tag by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses([tag_not_found, deletion_error, unexpected_error]),
)
async def delete_tag(
    use_case: Annotated[DeleteTagUseCase, Depends(delete_tag_use_case)],
    tag_id: int = Path(..., ge=1, description="ID of the tag to delete"),
):
    try:
        use_case.execute(tag_id)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Failed to execute request on Tag"
        ) from e
    except DeletionFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
