from datetime import datetime
import logging
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.src.domain.entities.role import Role
from app.src.domain.entities.tag import Tag
from app.src.domain.entities.user import User
from app.src.presentation.api.room_tag.room_tag_model import RoomTagModelResponse
from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.tag.create_tag_with_room_link_use_case import CreateTagWithRoomLinkUseCase
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
    TagCreateWithRoomLinkModelRequest,
    TagModelResponse,
    TagUpdateModelRequest,
    TagUpdateWithRoomLinkModelRequest,
)
from app.src.presentation.dependencies import (
    create_tag_use_case,
    create_tag_with_room_link_use_case,
    delete_tag_use_case,
    get_tag_by_id_use_case,
    get_tag_list_use_case,
    update_tag_use_case,
    update_tag_with_room_link_use_case,
)
from app.src.common.exception import (
    AlreadyExistsError,
    CheckConstraintError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)
from app.src.use_cases.tag.update_tag_with_room_link_use_case import UpdateTagWithRoomLinkUseCase

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
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
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


@tag_router.post(
    "/room",
    summary="Create a new tag and link it to a room",
    response_model=TagModelResponse,
    response_description="Details of the created room tag with its tag",
    responses=generate_responses([tag_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_tag_with_room_link(
    use_case: Annotated[CreateTagWithRoomLinkUseCase, Depends(create_tag_with_room_link_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    payload: Annotated[TagCreateWithRoomLinkModelRequest, Body(embed=True)],
):
    """
    Create a new tag and immediately link it to a room

    - **name**: Name of the tag
    - **description**: Optional description
    - **source_address**: Unique identifier for the tag source
    - **room_id**: ID of the room
    - **start_at** / **end_at**: Optional availability period
    """
    try:
        tag_entity = Tag(
            id=None,
            name=payload.name,
            description=payload.description,
            source_address=payload.source_address,
            created_at=None,
            updated_at=None,
        )

        new_tag: Tag = use_case.execute(tag_entity, payload.room_id, start_at=payload.start_at, end_at=payload.end_at)
        return TagModelResponse(**new_tag.to_dict())

    except CheckConstraintError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)
        ) from e
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except CreationFailedError as e:
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
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int | None = Query(20, ge=1, description="Number of elements return"),
    with_rooms: bool = Query(False, description="Include rooms and buildings"),
):
    """
    Retrieve a list of tags

    - **cursor**: Optional cursor for pagination (returns tags with id >= cursor)
    - **limit**: Number of tags to return (default: 20)
    - **with_rooms**: If true, include related rooms and buildings
    """
    try:
        result = use_case.execute(cursor, limit, with_rooms=with_rooms)

        metadata = PaginationMetadataModel(
            total=result.total,
            chunk_size=result.chunk_size,
            chunk_count=result.chunk_count,
            current_cursor=result.current_cursor,
            first_cursor=result.first_cursor,
            last_cursor=result.last_cursor,
            next_cursor=result.next_cursor,
        )

        tag_models = [TagModelResponse(**tag.to_dict()) for tag in result.tags]
        return PaginatedListTagModelResponse(data=tag_models, metadata=metadata)

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
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    tag_id: int = Path(..., ge=1, description="The tag ID (positive integer)"),
    with_rooms: bool = Query(False, description="Include rooms and buildings"),
):
    """
    Retrieve a tag by its unique identifier

    - **tag_id**: Must be a positive integer (≥ 1)
    - **with_rooms**: If true, include related rooms and buildings
    """
    try:
        tag_entity: Tag = use_case.execute(tag_id, with_rooms=with_rooms)

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
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
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
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
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
    


@tag_router.patch(
    "/{tag_id}/room",
    summary="Update a tag and its link with a room",
    response_model=TagModelResponse,
    response_description="Details of the updated room tag with its tag",
    responses=generate_responses([tag_not_found, update_error, unexpected_error]),
    deprecated=False,
)
async def update_tag_with_room_link(
    tag_id: int,
    use_case: Annotated[UpdateTagWithRoomLinkUseCase, Depends(update_tag_with_room_link_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    payload: Annotated[TagUpdateWithRoomLinkModelRequest, Body(embed=True)],
):
    """
    Update a tag and manage its link with a room

    - **name**: New tag name
    - **description**: Optional description
    - **source_address**: Unique identifier for the tag source
    - **room_id**: ID of the room (optional)
    - **start_at** / **end_at**: Availability period
    """
    try:
        update_data = payload.model_dump(exclude_unset=True)
        updated_tag: Tag = use_case.execute(
            tag_id=tag_id,
            update_data=update_data,
            room_id=payload.room_id,
            start_at=payload.start_at,
            end_at=payload.end_at
        )
        return TagModelResponse(**updated_tag.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except UpdateFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except CheckConstraintError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
