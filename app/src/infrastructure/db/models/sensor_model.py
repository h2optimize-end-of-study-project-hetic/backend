from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, TIMESTAMP


class SensorTemperatureModel(SQLModel, table=True):
    __tablename__ = "sensor_temperature"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: int | None = Field(default=None, nullable=True)
    host: str | None = Field(default=None, nullable=True)
    source_address: str | None = Field(default=None, nullable=True)
    temperature: float | None = Field(default=None, nullable=True)
    event_id: int | None = Field(default=None, nullable=True)
    relevance: float | None = Field(default=1.0, nullable=True)


class SensorHumidityModel(SQLModel, table=True):
    __tablename__ = "sensor_humidity"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: int | None = Field(default=None, nullable=True)
    source_address: str | None = Field(default=None, nullable=True)
    humidity: float | None = Field(default=None, nullable=True)
    event_id: int | None = Field(default=None, nullable=True)
    relevance: float | None = Field(default=1.0, nullable=True)


class SensorMotionModel(SQLModel, table=True):
    __tablename__ = "sensor_motion"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: int | None = None
    host: str | None = None
    source_address: str | None = None
    state: str | None = None
    move_duration: int | None = None
    move_number: int | None = None
    x_axis: int | None = None
    y_axis: int | None = None
    z_axis: int | None = None
    event_id: int | None = None
    relevance: float = 1.0


class SensorNeighborsCountModel(SQLModel, table=True):
    __tablename__ = "sensor_neighbors_count"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: int | None = None
    host: str | None = None
    source_address: str | None = None
    neighbors: int
    event_id: int | None = None
    relevance: float = 1.0


class SensorNeighborsDetailModel(SQLModel, table=True):
    __tablename__ = "sensor_neighbors_detail"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: int | None = None
    host: str | None = None
    source_address: str | None = None
    neighbor_address: str | None = None
    rssi: int | None = None
    tx_power: int | None = None
    event_id: int | None = None
    relevance: float = 1.0


class SensorPressureModel(SQLModel, table=True):
    __tablename__ = "sensor_pressure"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: int | None = Field(default=None, nullable=True)
    host: str | None = Field(default=None, nullable=True)
    source_address: str | None = Field(default=None, nullable=True)
    atmospheric_pressure: int | None = Field(default=None, nullable=True)
    event_id: int | None = Field(default=None, nullable=True)
    relevance: float | None = Field(default=1.0, nullable=True)


class SensorVoltageModel(SQLModel, table=True):
    __tablename__ = "sensor_voltage"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: int | None = None
    host: str | None = None
    source_address: str | None = None
    voltage: float
    event_id: int | None = None
    relevance: float = 1.0


class SensorButtonModel(SQLModel, table=True):
    __tablename__ = "sensor_button"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: int | None = None
    host: str | None = None
    source_address: str | None = None
    button: int
    event_id: int | None = None
    relevance: float = 1.0
