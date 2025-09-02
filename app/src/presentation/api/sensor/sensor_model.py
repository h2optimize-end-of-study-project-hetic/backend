from pydantic import BaseModel, Field


class SensorBaseModel(BaseModel):
    sensor_type: str = Field(..., min_length=1, max_length=255)
    value: float = Field(..., description="Measured value")


class SensorCreateModel(SensorBaseModel):
    pass


class SensorUpdateModel(BaseModel):
    sensor_type: str | None = Field(default=None, min_length=1, max_length=255)
    value: float | None = None


class SensorBaseModelResponse(BaseModel):
    id: int
    sensor_type: str
    value: float
    recorded_at: str


class SensorModel(SensorBaseModel):
    id: int
    recorded_at: str


class PaginatedSensorsModel(BaseModel):
    data: list[SensorBaseModelResponse]
    count: int
    offset: int
    limit: int
