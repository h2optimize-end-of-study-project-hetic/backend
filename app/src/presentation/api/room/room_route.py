import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.src.domain.entities.role import Role
from app.src.domain.entities.room import Room
from app.src.domain.entities.user import User
from app.src.presentation.api.common.generic_model import OffsetBasePaginationMetadataModel
from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.use_cases.room.create_room_use_case import CreateRoomUseCase
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses
from app.src.presentation.api.room.room_model import (
    PaginatedListRoomModelResponse,
    RoomCreateModelRequest,
    RoomModelResponse,
    RoomUpdateModelRequest,
)
from app.src.presentation.dependencies import (
    create_room_use_case,
    delete_room_use_case,
    get_room_by_id_use_case,
    get_room_list_use_case,
    update_room_use_case
)
from app.src.common.exception import (
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError
)
from app.src.use_cases.room.delete_room_use_case import DeleteRoomUseCase
from app.src.use_cases.room.get_room_by_id_use_case import GetRoomByIdUseCase
from app.src.use_cases.room.get_room_list_use_case import GetRoomListUseCase
from app.src.use_cases.room.update_room_use_case import UpdateRoomUseCase

creation_error = OpenApiErrorResponseConfig(code=406, description="Creation fails", detail="Failed to create Room")
building_not_found = OpenApiErrorResponseConfig(code=400, description="Building not found" , detail='Building not found')
room_not_found = OpenApiErrorResponseConfig(code=404, description="Room not found", detail="Room with ID '123' not found")
room_already_exist = OpenApiErrorResponseConfig(
    code=409, description="Room already exists", detail="Room with source_address '18458426' already exists"
)
update_error = OpenApiErrorResponseConfig(code=406, description="Update fails", detail="Failed to upadte Room")
deletion_error = OpenApiErrorResponseConfig(code=406, description="Deletion fails", detail="Failed to delete Room")
unexpected_error = OpenApiErrorResponseConfig(code=500, description="Unexpected error", detail="Internal server error")


logger = logging.getLogger(__name__)
room_router = APIRouter(
    prefix=f"/{OpenApiTags.room.value}", tags=[OpenApiTags.room]
) 


@room_router.post(
    "",
    summary="Create a new room",
    response_model=RoomModelResponse,
    response_description="Details of the created room",
    responses=generate_responses([creation_error, unexpected_error, building_not_found]),
    deprecated=False,
)
async def create_room(
    use_case: Annotated[CreateRoomUseCase, Depends(create_room_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    room: Annotated[RoomCreateModelRequest, Body(embed=True)],
):
    """
    Create a new room

    - **name**: Name of the room (minimum 3 characters, maximum 255 characters)
    - **description**: Optional description of the room
    - **floor**: Floor number where the room is located
    - **building_id**: ID of the building
    - **area**: Area in square meters
    - **shape**: Coordinates representing the shape of the room
    - **capacity**: Maximum number of people allowed
    - **start_at**: Optional start availability
    - **end_at**: Optional end availability
    """

    try:
        room_entity = Room(
            id=None,
            name=room.name,
            description=room.description,
            floor=room.floor,
            building_id=room.building_id,
            area=room.area,
            shape=room.shape,
            capacity=room.capacity,
            start_at=room.start_at,
            end_at=room.end_at,
            created_at=None,
            updated_at=None,
        )

        new_room: Room = use_case.execute(room_entity)

        return RoomModelResponse(**new_room.to_dict())
    
    except ForeignKeyConstraintError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Building not found'
        ) from e

    except CreationFailedError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Internal server error"
        ) from e



@room_router.get(
    "",
    summary="Retrieve a list of rooms",
    response_model=PaginatedListRoomModelResponse,
    response_description="Paginated list of rooms with metadata",
    responses=generate_responses([unexpected_error]),
    deprecated=False,
)
async def read_room_list(
    use_case: Annotated[GetRoomListUseCase, Depends(get_room_list_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    offset: int | None = Query(0, ge=0, description="Offset for pagination"),
    limit: int | None = Query(20, ge=1, description="Number of elements to return"),
):
    """
    Retrieve a paginated list of rooms

    - **offset**: starting index (default: 0)
    - **limit**: number of rooms per page (default: 20)
    """
    try:
        result = use_case.execute(offset=offset, limit=limit)

        room_models = [RoomModelResponse(**room.to_dict()) for room in result.rooms]

        metadata = OffsetBasePaginationMetadataModel(
            total=result.total,
            offset=result.offset,
            limit=result.limit,
            chunk_count=(result.total // result.limit) + (1 if result.total % result.limit else 0),
            order_by=result.order_by,
            order_direction=result.order_direction,
        )

        return PaginatedListRoomModelResponse(data=room_models, metadata=metadata)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) from e



@room_router.get(
    "/{room_id}",
    summary="Retrieve room by ID",
    response_model=RoomModelResponse,
    response_description="Detailed information of the requested room",
    responses=generate_responses([room_not_found, unexpected_error]),
    deprecated=False,
)
async def read_room(
    use_case: Annotated[GetRoomByIdUseCase, Depends(get_room_by_id_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    room_id: int = Path(..., ge=1, description="The room ID (positive integer)"),
):
    """
    Retrieve a room by its unique identifier

    - **room_id**: Must be a positive integer (≥ 1)
    """
    try:
        room_entity: Room = use_case.execute(room_id)

        return RoomModelResponse(**room_entity.to_dict())

    except NotFoundError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@room_router.patch(
    "/{room_id}",
    summary="Update a room partially",
    response_model=RoomModelResponse,
    response_description="Details of the updated room",
    responses=generate_responses([room_not_found, update_error, unexpected_error, building_not_found]),
)
async def update_room(
    use_case: Annotated[UpdateRoomUseCase, Depends(update_room_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    room: Annotated[RoomUpdateModelRequest, Body(embed=True)],
    room_id: int = Path(..., ge=1, description="ID of the room to update"),
):
    """
    Update a room partially

    - **name**: Name of the room (minimum 3 characters, maximum 255 characters)
    - **description**: Optional description of the room
    - **floor**: Floor number where the room is located
    - **building_id**: ID of the building
    - **area**: Area in square meters
    - **shape**: Coordinates representing the shape of the room
    - **capacity**: Maximum number of people allowed
    - **start_at**: Optional start availability
    - **end_at**: Optional end availability
    """

    try:
        update_data = room.model_dump(exclude_unset=True)

        updated_room: Room = use_case.execute(room_id, update_data)

        return RoomModelResponse(**updated_room.to_dict())

    except NotFoundError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Building not found'
        ) from e
    except UpdateFailedError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e


@room_router.delete(
    "/{room_id}",
    summary="Delete a room by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses([room_not_found, deletion_error, unexpected_error]),
)
async def delete_room(
    use_case: Annotated[DeleteRoomUseCase, Depends(delete_room_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    room_id: int = Path(..., ge=1, description="ID of the room to delete"),
):
    """
    Delete a room by its unique identifier

    - **room_id**: Must be a positive integer (≥ 1)
    """
        
    try:
        use_case.execute(room_id)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ForeignKeyConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Failed to execute request on Room"
        ) from e
    except DeletionFailedError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
