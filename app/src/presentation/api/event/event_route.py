import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

<<<<<<< HEAD
<<<<<<< HEAD
from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User

=======
>>>>>>> aa712d6 (crud event)
=======
>>>>>>> 862071b (crud event)
from app.src.domain.entities.event import Event
from app.src.presentation.core.open_api_events import OpenApiEvents
from app.src.use_cases.event.delete_event_use_case import DeleteEventUseCase
from app.src.use_cases.event.update_event_use_case import UpdateEventUseCase
from app.src.use_cases.event.create_event_use_case import CreateEventUseCase
from app.src.use_cases.event.get_event_list_use_case import GetEventListUseCase
from app.src.use_cases.event.get_event_by_id_use_case import GetEventByIdUseCase
from app.src.presentation.api.common.generic_model import PaginationMetadataModel
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.presentation.api.event.event_model import (
    PaginatedListEventModelResponse,
    EventCreateModelRequest,
    EventModelResponse,
    EventUpdateModelRequest,
)
from app.src.presentation.dependencies import (
    create_event_use_case,
    delete_event_use_case,
    get_event_by_id_use_case,
    get_event_list_use_case,
    update_event_use_case,
)
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

event_not_found = OpenApiErrorResponseConfig(code=404, description="Event not found", detail="Event with ID '123' not found")
event_already_exist = OpenApiErrorResponseConfig(
    code=409, description="Event already exists", detail="Event with file_name 'Building A - Floor 1' already exists"
)
creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Failed to create Event")
update_error = OpenApiErrorResponseConfig(code=406, description="Update fails", detail="Failed to update Event")
deletion_error = OpenApiErrorResponseConfig(code=406, description="Deletion fails", detail="Failed to delete Event")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")


logger = logging.getLogger(__name__)
event_router = APIRouter(
    prefix=f"/{OpenApiEvents.event.value}", tags=[OpenApiEvents.event]
)  # events and OpenApiEvents are not bind to the entity event. It's just the param of APIRouter


@event_router.post(
    "",
    summary="Create a new event",
    response_model=EventModelResponse,
    response_description="Details of the created event",
    responses=generate_responses([event_already_exist, creation_error, unexpected_error]),
    deprecated=False,
)
async def create_event(
    use_case: Annotated[CreateEventUseCase, Depends(create_event_use_case)],
    event: Annotated[EventCreateModelRequest, Body(embed=True)],
):
    """
    Create a new event

    - **name**: Name of the event (minimum 3 characters, maximum 255 characters)
    - **description**: Description of the event
    - **group_id** : The group ID to which this event is attached to
    - **supervisor** : The name of the supervisor of the event
    """
    try:
        event_entity = Event(
            id=None,
            name=event.name,
            description=event.description,
            group_id=event.group_id,
            supervisor=event.supervisor,
            created_at=None,
            updated_at=None,
        )

        new_event: Event = use_case.execute(event_entity)

        return EventModelResponse(**new_event.to_dict())

    except AlreadyExistsError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@event_router.get(
    "",
    summary="Retrieve a list of events",
    response_model=PaginatedListEventModelResponse,
    response_description="Detailed information of the requested events",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_event_list(
    use_case: Annotated[GetEventListUseCase, Depends(get_event_list_use_case)],
<<<<<<< HEAD
<<<<<<< HEAD
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
=======
>>>>>>> aa712d6 (crud event)
=======
>>>>>>> 862071b (crud event)
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int | None = Query(20, ge=1, description="Number of elements return"),
):
    """
    Retrieve a list of events

    - **cursor**: Optional cursor for pagination (returns events with id >= cursor)
    - **limit**: Number of events to return (default: 20)
    """
    try:
        result = use_case.execute(cursor, limit)

        event_models = [EventModelResponse(**event.to_dict()) for event in result.events]

        metadata = PaginationMetadataModel(
            total=result.total,
            chunk_size=result.chunk_size,
            chunk_count=result.chunk_count,
            current_cursor=result.current_cursor,
            first_cursor=result.first_cursor,
            last_cursor=result.last_cursor,
            next_cursor=result.next_cursor,
        )

        response = PaginatedListEventModelResponse(data=event_models, metadata=metadata)

        return response

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@event_router.get(
    "/{event_id}",
    summary="Retrieve event info by ID",
    response_model=EventModelResponse,
    response_description="Detailed information of the requested event",
    responses=generate_responses([event_not_found, unexpected_error]),
    deprecated=False,
)

async def read_event(
    use_case: Annotated[GetEventByIdUseCase, Depends(get_event_by_id_use_case)],
<<<<<<< HEAD
<<<<<<< HEAD
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
=======
>>>>>>> aa712d6 (crud event)
=======
>>>>>>> 862071b (crud event)
    event_id: int = Path(..., ge=1, description="The event ID (positive integer)"),
):
    """
    Retrieve a event by its unique identifier

    - **event_id**: Must be a positive integer (≥ 1)
    """
    try:
        event_entity: Event = use_case.execute(event_id)

        return EventModelResponse(**event_entity.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@event_router.patch(
    "/{event_id}",
    summary="Update a event partially",
    response_model=EventModelResponse,
    responses=generate_responses([event_not_found, event_already_exist, unexpected_error]),
)
async def update_event(
    use_case: Annotated[UpdateEventUseCase, Depends(update_event_use_case)],
<<<<<<< HEAD
<<<<<<< HEAD
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
=======
    # file: Annotated[UploadFile | None, File()] = None,
>>>>>>> aa712d6 (crud event)
=======
    # file: Annotated[UploadFile | None, File()] = None,
>>>>>>> 862071b (crud event)
    event: Annotated[EventUpdateModelRequest, Body(embed=True)],
    event_id: int = Path(..., ge=1, description="ID of the event to update"),
):
    try:
        update_data = event.model_dump(exclude_unset=True)
        updated_event = use_case.execute(event_id, update_data)

        return EventModelResponse(**updated_event.to_dict())

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except UpdateFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@event_router.delete(
    "/{event_id}",
    summary="Delete a event by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses([event_not_found, deletion_error, unexpected_error]),
)
async def delete_event(
    use_case: Annotated[DeleteEventUseCase, Depends(delete_event_use_case)],
<<<<<<< HEAD
<<<<<<< HEAD
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
=======
>>>>>>> aa712d6 (crud event)
=======
>>>>>>> 862071b (crud event)
    event_id: int = Path(..., ge=1, description="ID of the event to delete"),
):
    try:
        use_case.execute(event_id)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Failed to execute request on Event"
        ) from e
    except DeletionFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
