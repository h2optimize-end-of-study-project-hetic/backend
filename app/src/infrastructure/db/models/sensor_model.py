from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, TIMESTAMP, text


class SensorTemperatureModel(SQLModel, table=True):
    __tablename__ = "sensor_temperature"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    temperature: float
    event_id: Optional[int] = None
    relevance: float = 1.0


class SensorHumidityModel(SQLModel, table=True):
    __tablename__ = "sensor_humidity"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    source_address: Optional[str] = None
    humidity: float
    event_id: Optional[int] = None
    relevance: float = 1.0


class SensorMotionModel(SQLModel, table=True):
    __tablename__ = "sensor_motion"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    state: Optional[str] = None
    move_duration: Optional[int] = None
    move_number: Optional[int] = None
    x_axis: Optional[int] = None
    y_axis: Optional[int] = None
    z_axis: Optional[int] = None
    event_id: Optional[int] = None
    relevance: float = 1.0


class SensorNeighborsCountModel(SQLModel, table=True):
    __tablename__ = "sensor_neighbors_count"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    neighbors: int
    event_id: Optional[int] = None
    relevance: float = 1.0


class SensorNeighborsDetailModel(SQLModel, table=True):
    __tablename__ = "sensor_neighbors_detail"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    neighbor_address: Optional[str] = None
    rssi: Optional[int] = None
    tx_power: Optional[int] = None
    event_id: Optional[int] = None
    relevance: float = 1.0


class SensorPressureModel(SQLModel, table=True):
    __tablename__ = "sensor_pressure"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    atmospheric_pressure: int
    event_id: Optional[int] = None
    relevance: float = 1.0


class SensorVoltageModel(SQLModel, table=True):
    __tablename__ = "sensor_voltage"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    voltage: float
    event_id: Optional[int] = None
    relevance: float = 1.0


class SensorButtonModel(SQLModel, table=True):
    __tablename__ = "sensor_button"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    button: int
    event_id: Optional[int] = None
    relevance: float = 1.0
