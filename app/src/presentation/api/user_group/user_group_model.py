from datetime import datetime

from pydantic import BaseModel, Field

from app.src.presentation.api.common.generic_model import PaginationMetadataModel


class UserGroupBaseModel(BaseModel):
    group_id: int = Field (
        default=None, title="Group ID", gt=0, description="The group ID of the user"
    )
    user_id: int = Field (
        default=None, title="User ID", gt=0, description="The user ID of the user"
    )


class UserGroupCreateModelRequest(UserGroupBaseModel):
    pass


class UserGroupUpdateModelRequest(BaseModel):
    group_id: int | None = Field (
        default=None, title="Group ID", gt=0, description="The group ID of the user"
    )
    user_id: int | None = Field (
        default=None, title="User ID", gt=0, description="The user ID of the user"
    )


class UserGroupModelResponse(UserGroupBaseModel):
    id: int
    created_at: datetime | None
    updated_at: datetime | None


class PaginatedListUserGroupModelResponse(BaseModel):
    data: list[UserGroupModelResponse]
    metadata: PaginationMetadataModel
