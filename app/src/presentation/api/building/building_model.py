from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field
from app.src.presentation.api.common.generic_model import PaginationMetadataModel


class BuildingBaseModel(BaseModel):
    name: str = Field (
        default=None, title="Name", description="The name of the building"
    )
    description: str = Field (
        default=None, title="Description", description="The description of the building"
    )
    room_count: int = Field (
        default=None, gt=0, title="Room count", description="The number of room in the building"
    )
    street_number: str = Field (
        default=None, title="Street number", description="The number street where the building is located"
    )
    street_name: str = Field (
        default=None, title="Street name", description="The name of the street where the building is located"
    )
    postal_code: str = Field (
        default=None, title="Postal code", description="The postal code of the building"
    )
    city: str = Field (
        default=None, title="City", description="The city where the building is"
    )
    country: str = Field (
        default=None, title="Country", description="The country where the building is"
    )
    latitude: Decimal = Field (
        default=None, title="Latitude", description="The latitude where the building is"
    )
    longitude: Decimal = Field (
        default=None, title="Longitude", description="The longitude where the building is"
    )

    class Config:
        orm_mode = True
        json_encoders = {
            Decimal: lambda v: float(v) if v is not None else None,
        }

class BuildingCreateModelRequest(BuildingBaseModel):
    pass


class BuildingUpdateModelRequest(BaseModel):
    name: str | None = Field (
        default=None, title="Name", description="The name of the building"
    )
    description: str | None = Field (
        default=None, title="Description", description="The description of the building"
    )
    room_count: int | None = Field (
        default=None, gt=0, title="Room count", description="The number of room in the building"
    )
    street_number: str | None = Field (
        default=None, title="Street number", description="The number street where the building is located"
    )
    street_name: str | None = Field (
        default=None, title="Street name", description="The name of the street where the building is located"
    )
    postal_code: str | None = Field (
        default=None, title="Postal code", description="The postal code of the building"
    )
    city: str | None = Field (
        default=None, title="City", description="The city where the building is"
    )
    country: str | None = Field (
        default=None, title="Country", description="The country where the building is"
    )
    latitude: Decimal | None = Field (
        default=None, title="Latitude", description="The latitude where the building is"
    )
    longitude: Decimal | None = Field (
        default=None, title="Longitude", description="The longitude where the building is"
    )

class BuildingModelResponse(BuildingBaseModel):
    id: int
    created_at: datetime | None
    updated_at: datetime | None


class PaginatedListBuildingModelResponse(BaseModel):
    data: list[BuildingModelResponse]
    metadata: PaginationMetadataModel
