from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SensorBaseModel(BaseModel):
    time: datetime = Field(..., description="Timestamp of the measurement")
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    event_id: Optional[int] = None
    relevance: float = 1.0


class SensorButtonModelResponse(SensorBaseModel):
    button: Optional[int] = None


class SensorHumidityModelResponse(SensorBaseModel):
    humidity: float


class SensorMotionModelResponse(SensorBaseModel):
    state: Optional[str] = None
    move_duration: Optional[int] = None
    move_number: Optional[int] = None
    x_axis: Optional[int] = None
    y_axis: Optional[int] = None
    z_axis: Optional[int] = None


class SensorNeighborsCountModelResponse(SensorBaseModel):
    neighbors: Optional[int] = None


class SensorNeighborsDetailModelResponse(SensorBaseModel):
    neighbor_address: Optional[str] = None
    rssi: Optional[int] = None
    tx_power: Optional[int] = None


class SensorPressureModelResponse(SensorBaseModel):
    atmospheric_pressure: Optional[int] = None


class SensorTemperatureModelResponse(SensorBaseModel):
    temperature: float


class SensorVoltageModelResponse(SensorBaseModel):
    voltage: float


class PaginatedSensorsModel(BaseModel):
    data: list[SensorBaseModel]
    count: int
    offset: int
    limit: int
