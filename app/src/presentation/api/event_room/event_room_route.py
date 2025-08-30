import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.domain.entities.event_room import EventRoom
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.event_room.delete_event_room_use_case import DeleteEventRoomUseCase
from app.src.use_cases.event_room.update_event_room_use_case import UpdateEventRoomUseCase
from app.src.use_cases.event_room.create_event_room_use_case import CreateEventRoomUseCase
from app.src.use_cases.event_room.get_event_room_list_use_case import GetEventRoomListUseCase
from app.src.use_cases.event_room.get_event_room_by_id_use_case import GetEventRoomByIdUseCase
from app.src.presentation.api.common.generic_model import PaginationMetadataModel
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.presentation.api.event_room.event_room_model import (
    PaginatedListEventRoomModelResponse,
    EventRoomCreateModelRequest,
    EventRoomModelResponse,
    EventRoomUpdateModelRequest,
)
from app.src.presentation.dependencies import (
    create_event_room_use_case,
    delete_event_room_use_case,
    get_event_room_by_id_use_case,
    get_event_room_list_use_case,
    update_event_room_use_case,
)
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

event_room_not_found = OpenApiErrorResponseConfig(code=404, description="EventRoom not found", detail="EventRoom with ID '123' not found")
event_room_already_exist = OpenApiErrorResponseConfig(
    code=409, description="EventRoom already exists", detail="EventRoom with file_name 'Building A - Floor 1' already exists"
)
creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Failed to create EventRoom")
update_error = OpenApiErrorResponseConfig(code=406, description="Update fails", detail="Failed to update EventRoom")
deletion_error = OpenApiErrorResponseConfig(code=406, description="Deletion fails", detail="Failed to delete EventRoom")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")


logger = logging.getLogger(__name__)
event_room_router = APIRouter(
    prefix=f"/{OpenApiTags.event_room.value}", tags=[OpenApiTags.event_room]
)  # event_rooms and OpenApiEventRooms are not bind to the entity event_room. It's just the param of APIRouter


@event_room_router.post(
    "",
    summary="Create a new event_room",
    response_model=EventRoomModelResponse,
    response_description="Details of the created event_room",
    responses=generate_responses([event_room_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_event_room(
    use_case: Annotated[CreateEventRoomUseCase, Depends(create_event_room_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    event_room: Annotated[EventRoomCreateModelRequest, Body(embed=True)],

):
    """
    Create a new event_room

    - **room_id** : The room ID to which this event_room is attached to
    - **event_id** : The event ID to which this event_room is attached to
    - **is_finished**: If the event in the room is finished
    - **start_at**: The date when the event start in the room
    - **end_at** : The date when the event start in the room
    """
    try:
        event_room_entity = EventRoom(
            id=None,
            room_id=event_room.room_id,
            event_id=event_room.event_id,
            is_finished=event_room.is_finished,
            start_at=event_room.start_at,
            end_at=event_room.end_at,
            created_at=None,
            updated_at=None,
        )

        new_event_room: EventRoom = use_case.execute(event_room_entity)

        return EventRoomModelResponse(**new_event_room.to_dict())

    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@event_room_router.get(
    "",
    summary="Retrieve a list of event_rooms",
    response_model=PaginatedListEventRoomModelResponse,
    response_description="Detailed information of the requested event_rooms",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_event_room_list(
    use_case: Annotated[GetEventRoomListUseCase, Depends(get_event_room_list_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int | None = Query(20, ge=1, description="Number of elements return"),
):
    """
    Retrieve a list of event_rooms

    - **cursor**: Optional cursor for pagination (returns event_rooms with id >= cursor)
    - **limit**: Number of event_rooms to return (default: 20)
    """
    try:
        result = use_case.execute(cursor, limit)

        event_room_models = [EventRoomModelResponse(**event_room.to_dict()) for event_room in result.event_rooms]

        metadata = PaginationMetadataModel(
            total=result.total,
            chunk_size=result.chunk_size,
            chunk_count=result.chunk_count,
            current_cursor=result.current_cursor,
            first_cursor=result.first_cursor,
            last_cursor=result.last_cursor,
            next_cursor=result.next_cursor,
        )

        response = PaginatedListEventRoomModelResponse(data=event_room_models, metadata=metadata)

        return response

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@event_room_router.get(
    "/{event_room_id}",
    summary="Retrieve event_room info by ID",
    response_model=EventRoomModelResponse,
    response_description="Detailed information of the requested event_room",
    responses=generate_responses([event_room_not_found, unexpected_error]),
    deprecated=False,
)
async def read_event_room(
    use_case: Annotated[GetEventRoomByIdUseCase, Depends(get_event_room_by_id_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    event_room_id: int = Path(..., ge=1, description="The event_room ID (positive integer)"),
):
    """
    Retrieve a event_room by its unique identifier

    - **event_room_id**: Must be a positive integer (≥ 1)
    """
    try:
        event_room_entity: EventRoom = use_case.execute(event_room_id)

        return EventRoomModelResponse(**event_room_entity.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@event_room_router.patch(
    "/{event_room_id}",
    summary="Update a event_room partially",
    response_model=EventRoomModelResponse,
    responses=generate_responses([event_room_not_found, event_room_already_exist, unexpected_error]),
)
async def update_event_room(
    use_case: Annotated[UpdateEventRoomUseCase, Depends(update_event_room_use_case)],
    event_room: Annotated[EventRoomUpdateModelRequest, Body(embed=True)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    event_room_id: int = Path(..., ge=1, description="ID of the event_room to update"),
):
    try:
        update_data = event_room.model_dump(exclude_unset=True)
        updated_event_room = use_case.execute(event_room_id, update_data)

        return EventRoomModelResponse(**updated_event_room.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except UpdateFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@event_room_router.delete(
    "/{event_room_id}",
    summary="Delete a event_room by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses([event_room_not_found, deletion_error, unexpected_error]),
)
async def delete_event_room(
    use_case: Annotated[DeleteEventRoomUseCase, Depends(delete_event_room_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    event_room_id: int = Path(..., ge=1, description="ID of the event_room to delete"),
):
    try:
        use_case.execute(event_room_id)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Failed to execute request on EventRoom"
        ) from e
    except DeletionFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
