from datetime import datetime

from pydantic import BaseModel, Field

from app.src.presentation.api.common.generic_model import PaginationMetadataModel


class EventRoomBaseModel(BaseModel):
    room_id: int = Field (
        default=None, title="Room ID", gt=0, description="The room ID to which this event_room is attached to"
    )
    event_id: int = Field (
        default=None, title="Event ID", gt=0, description="The event ID to which this event_room is attached to"
    )
    is_finished: bool = Field (
        default=False, title="is_finished", description="Is the event_room done"
    )
    start_at: datetime = Field (
        default=None, title="start_at", description="When the event in this room start"
    )
    end_at: datetime = Field (
        default=None, title="end_at", description="When the event in this room end"
    )


class EventRoomCreateModelRequest(EventRoomBaseModel):
    pass


class EventRoomUpdateModelRequest(BaseModel):
    room_id: int | None = Field (
        default=None, title="Room ID", gt=0, description="The room ID to which this event_room is attached to"
    )
    event_id: int | None = Field (
        default=None, title="Event ID", gt=0, description="The event ID to which this event_room is attached to"
    )
    is_finished: bool | None = Field (
        default=False, title="is_finished", description="Is the event_room done"
    )
    start_at: datetime | None = Field (
        default=None, title="start_at", description="When the event in this room start"
    )
    end_at: datetime | None = Field (
        default=None, title="end_at", description="When the event in this room end"
    )

class EventRoomModelResponse(EventRoomBaseModel):
    id: int
    created_at: datetime | None
    updated_at: datetime | None


class PaginatedListEventRoomModelResponse(BaseModel):
    data: list[EventRoomModelResponse]
    metadata: PaginationMetadataModel
