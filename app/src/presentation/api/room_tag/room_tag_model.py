from datetime import datetime

from pydantic import BaseModel, Field

from app.src.presentation.api.common.generic_model import PaginationMetadataModel


class RoomTagBaseModel(BaseModel):
    tag_id: int = Field(default=1, ge=1, title="Tag ID", description="Identifier of the tag")
    room_id: int = Field(default=1, ge=1, title="Room ID", description="Identifier of the Room")
    start_at: datetime | None = Field(default=None, title="Start availability", description="When the room is available from")
    end_at: datetime | None = Field(default=None, title="End availability", description="When the room is available until")


class RoomTagCreateModelRequest(RoomTagBaseModel):
    pass

class RoomTagUpdateModelRequest(BaseModel):
    tag_id: int | None = Field(default=None, ge=1, title="Tag ID", description="Identifier of the tag")
    room_id: int | None = Field(default=None, ge=1, title="Room ID", description="Identifier of the Room")
    start_at: datetime | None = Field(default=None, title="Start availability", description="When the room is available from")
    end_at: datetime | None = Field(default=None, title="End availability", description="When the room is available until")

class RoomTagModelResponse(RoomTagBaseModel):
    id: int
    created_at: datetime | None
    updated_at: datetime | None


class PaginatedListRoomTagModelResponse(BaseModel):
    data: list[RoomTagModelResponse]
    metadata: PaginationMetadataModel
