from datetime import datetime

from pydantic import BaseModel, Field

from app.src.presentation.api.common.generic_model import PaginationMetadataModel


class GroupBaseModel(BaseModel):
    name: str = Field (
        default=None, title="Name", description="The name of the group"
    )
    description: str = Field (
        default=None, title="Description", description="The description of the group"
    )
    member_count: int = Field (
        default=None, gt=0, title="Member count", description="The number of user in the group"
    )
    start_at: datetime = Field (
        default=None, title="start_at", description="When the event in this room start"
    )
    end_at: datetime = Field (
        default=None, title="end_at", description="When the event in this room end"
    )


class GroupCreateModelRequest(GroupBaseModel):
    pass


class GroupUpdateModelRequest(BaseModel):
    name: str | None = Field (
        default=None, title="Name", description="The name of the group"
    )
    description: str | None = Field (
        default=None, title="Description", description="The description of the group"
    )
    member_count: int | None = Field (
        default=None, gt=0, title="Member count", description="The number of user in the group"
    )
    start_at: datetime | None = Field (
        default=None, title="start_at", description="When the event in this room start"
    )
    end_at: datetime | None = Field (
        default=None, title="end_at", description="When the event in this room end"
    )

class GroupModelResponse(GroupBaseModel):
    id: int
    created_at: datetime | None
    updated_at: datetime | None


class PaginatedListGroupModelResponse(BaseModel):
    data: list[GroupModelResponse]
    metadata: PaginationMetadataModel
