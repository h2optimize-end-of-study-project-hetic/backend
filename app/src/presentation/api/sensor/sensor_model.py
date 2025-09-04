from datetime import datetime
from typing import Optional, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, TIMESTAMP, text, JSON

# Bouton
class SensorButtonModel(SQLModel, table=True):
    __tablename__ = "sensor_button"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    button: Optional[int] = None
    event_id: Optional[int] = None
    relevance: float = 1.0


# Humidité (%)
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


# Mouvement
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


# Nombre de voisins
class SensorNeighborsCountModel(SQLModel, table=True):
    __tablename__ = "sensor_neighbors_count"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    neighbors: Optional[int] = None
    event_id: Optional[int] = None
    relevance: float = 1.0


# Détail des voisins
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


# Pression atmosphérique
class SensorPressureModel(SQLModel, table=True):
    __tablename__ = "sensor_pressure"

    time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    )
    sensor_id: Optional[int] = None
    host: Optional[str] = None
    source_address: Optional[str] = None
    atmospheric_pressure: Optional[int] = None
    event_id: Optional[int] = None
    relevance: float = 1.0


# Température
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


# Tension
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
