import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.src.domain.entities.tag import Tag
from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.domain.entities.room_tag import RoomTag
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.presentation.api.common.generic_model import PaginationMetadataModel
from app.src.use_cases.room_tag.delete_room_tag_use_case import DeleteRoomTagUseCase
from app.src.use_cases.room_tag.update_room_tag_use_case import UpdateRoomTagUseCase
from app.src.use_cases.room_tag.create_room_tag_use_case import CreateRoomTagUseCase
from app.src.use_cases.room_tag.get_room_tag_list_use_case import GetRoomTagListUseCase
from app.src.use_cases.room_tag.get_room_tag_by_id_use_case import GetRoomTagByIdUseCase
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.presentation.api.room_tag.room_tag_model import PaginatedListRoomTagModelResponse, RoomTagCreateModelRequest, RoomTagModelResponse, RoomTagUpdateModelRequest
from app.src.presentation.dependencies import (
    create_room_tag_use_case,
    delete_room_tag_use_case,
    get_room_tag_by_id_use_case,
    get_room_tag_list_use_case,
    update_room_tag_use_case,
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


room_tag_not_found = OpenApiErrorResponseConfig(code=404, description="Room Tag not found", detail="Tag with ID '123' not found")
room_tag_already_exist = OpenApiErrorResponseConfig(
    code=409, description="Room Tag already exists", detail="RoomTag with room_id, tag_id 'room_id=1 and tag_id=1' already exists"
)
creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Failed to create Room Tag")
update_error = OpenApiErrorResponseConfig(code=406, description="Update fails", detail="Failed to upadte Room Tag")
deletion_error = OpenApiErrorResponseConfig(code=406, description="Deletion fails", detail="Failed to delete Room Tag")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")


logger = logging.getLogger(__name__)
room_tag_router = APIRouter(
    prefix=f"/{OpenApiTags.room_tag.value}", tags=[OpenApiTags.room_tag]
)


@room_tag_router.post(
    "",
    summary="Create a new room tag",
    response_model=RoomTagModelResponse,
    response_description="Details of the created room tag",
    responses=generate_responses([room_tag_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_room_tag(
    use_case: Annotated[CreateRoomTagUseCase, Depends(create_room_tag_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    room_tag: Annotated[RoomTagCreateModelRequest, Body(embed=True)],
):
    """
    Create a new link between room and tag

    - **tag_id**: ID of the tag
    - **room_id**: ID of the room
    - **start_at**: Optional start availability
    - **end_at**: Optional end availability
    """
    try:
        room_tag_entity = RoomTag(
            id=None,
            tag_id=room_tag.tag_id,
            room_id=room_tag.room_id,
            start_at=room_tag.start_at,
            end_at=room_tag.end_at,
            created_at=None,
            updated_at=None,
        )

        new_room_tag: RoomTag = use_case.execute(room_tag_entity)

        return RoomTagModelResponse(**new_room_tag.to_dict())

    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except CheckConstraintError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)
        ) from e
    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e



@room_tag_router.get(
    "",
    summary="Retrieve a list of links between room and tag",
    response_model=PaginatedListRoomTagModelResponse,
    response_description="Detailed information of the requested links",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_room_tag_list(
    use_case: Annotated[GetRoomTagListUseCase, Depends(get_room_tag_list_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int | None = Query(20, ge=1, description="Number of elements return"),
    active_only: bool = Query(False, description="Return only currently active links"),
):
    """
    Retrieve a list of links between room and tag

    - **cursor**: Optional cursor for pagination (returns tags with id >= cursor)
    - **limit**: Number of tags to return (default: 20)
    - **active_only**: If true, return only links valid at the current time
    """
    try:
        result = use_case.execute(cursor, limit, active_only=active_only)

        room_tag_models = [RoomTagModelResponse(**room_tag.to_dict()) for room_tag in result.room_tag]

        metadata = PaginationMetadataModel(
            total=result.total,
            chunk_size=result.chunk_size,
            chunk_count=result.chunk_count,
            current_cursor=result.current_cursor,
            first_cursor=result.first_cursor,
            last_cursor=result.last_cursor,
            next_cursor=result.next_cursor,
        )

        response = PaginatedListRoomTagModelResponse(data=room_tag_models, metadata=metadata)
        return response

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@room_tag_router.get(
    "/{room_tag_id}",
    summary="Retrieve link between room and tag by ID",
    response_model=RoomTagModelResponse,
    response_description="Detailed information of the requested tag",
    responses=generate_responses([room_tag_not_found, unexpected_error]),
    deprecated=False,
)
async def read_tag(
    use_case: Annotated[GetRoomTagByIdUseCase, Depends(get_room_tag_by_id_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    room_tag_id: int = Path(..., ge=1, description="The ID of the link between room and tag(positive integer)"),
):
    """
    Retrieve a link between room and tag by unique identifier

    - **room_tag_id**: Must be a positive integer (≥ 1)
    """
    try:
        room_tag_entity: Tag = use_case.execute(room_tag_id)

        return RoomTagModelResponse(**room_tag_entity.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@room_tag_router.patch(
    "/{room_tag_id}",
    summary="Update the link between room and tag, partially",
    response_model=RoomTagModelResponse,
    responses=generate_responses([room_tag_not_found, unexpected_error]),
)
async def update_tag(
    use_case: Annotated[UpdateRoomTagUseCase, Depends(update_room_tag_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    room_tag: Annotated[RoomTagUpdateModelRequest, Body(embed=True)],
    room_tag_id: int = Path(..., ge=1, description="ID of the link between room and tag to update"),
):
    try:
        update_data = room_tag.model_dump(exclude_unset=True)
        updated_room_tag = use_case.execute(room_tag_id, update_data)

        return RoomTagModelResponse(**updated_room_tag.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except CheckConstraintError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)
        ) from e
    except UpdateFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@room_tag_router.delete(
    "/{room_tag_id}",
    summary="Delete the link between room and tag by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses([room_tag_not_found, deletion_error, unexpected_error]),
)
async def delete_tag(
    use_case: Annotated[DeleteRoomTagUseCase, Depends(delete_room_tag_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    room_tag_id: int = Path(..., ge=1, description="ID of the link between room and tag to delete"),
):
    try:
        use_case.execute(room_tag_id)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Failed to execute request on the link between room and tag"
        ) from e
    except DeletionFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
