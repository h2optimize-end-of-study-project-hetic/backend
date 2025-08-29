from datetime import datetime

from pydantic import BaseModel, Field

from app.src.presentation.api.common.generic_model import PaginationMetadataModel


class EventBaseModel(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        title="Name",
        description="The name of the event must be between 3 and 255 characters long",
    )
    description: str = Field(
        ..., min_length=3, title="Description", description="The description must be at least 3 characters long"
    )
    group_id: int = Field(
        default=None, gt=0, title="Group ID", description="The group to which the event is attached"
    )
    supervisor: str = Field(
        default=None, title="Supervisor", description="Name of the supervisor of the event"
    )


class EventCreateModelRequest(EventBaseModel):
    pass


class EventUpdateModelRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        title="Name",
        description="The name of the event must be between 3 and 255 characters long",
    )
    description: str | None = Field(
        default=None,
        min_length=3, 
        title="Description", 
        description="The description must be at least 3 characters long"
    )
    group_id: int | None = Field(
        default=None, gt=0, title="Group ID", description="The group to which the event is attached"
    )
    supervisor: str | None = Field(
        default=None, title="Supervisor", description="Name of the supervisor of the event"
    )


class EventModelResponse(EventBaseModel):
    id: int
    created_at: datetime | None
    updated_at: datetime | None


class PaginatedListEventModelResponse(BaseModel):
    data: list[EventModelResponse]
    metadata: PaginationMetadataModel
