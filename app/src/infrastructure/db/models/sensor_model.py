from datetime import datetime
from typing import Optional, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, TIMESTAMP, text, JSON


# Bouton: on stocke un booléen (pressé ou non)
class SensorButtonModel(SQLModel, table=True):
    __tablename__ = "sensor_button"
    id: int | None = Field(default=None, primary_key=True)
    value: bool = Field(default=False, nullable=False)
    recorded_at: datetime = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False),
    )


# Humidité (%)
class SensorHumidityModel(SQLModel, table=True):
    __tablename__ = "sensor_humidity"
    id: int | None = Field(default=None, primary_key=True)
    value: float = Field(..., nullable=False)
    recorded_at: datetime = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False),
    )


# Mouvement: booléen (détecté ou non)
class SensorMotionModel(SQLModel, table=True):
    __tablename__ = "sensor_motion"
    id: int | None = Field(default=None, primary_key=True)
    value: bool = Field(default=False, nullable=False)
    recorded_at: datetime = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False),
    )


# Voisinage: nombre de voisins
class SensorNeighborsCountModel(SQLModel, table=True):
    __tablename__ = "sensor_neighbors_count"
    id: int | None = Field(default=None, primary_key=True)
    count: int = Field(default=0, nullable=False)
    recorded_at: datetime = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False),
    )


# Détail du voisinage: JSON flexible (ids, RSSI, etc.)
class SensorNeighborsDetailModel(SQLModel, table=True):
    __tablename__ = "sensor_neighbors_detail"
    id: int | None = Field(default=None, primary_key=True)
    data: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    recorded_at: datetime = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False),
    )


# Pression (hPa)
class SensorPressureModel(SQLModel, table=True):
    __tablename__ = "sensor_pressure"
    __table_args__ = {"extend_existing": True}

    source_address: str = Field(default="", nullable=False, primary_key=True)
    atmospheric_pressure: float = Field(..., nullable=False)
    time: datetime = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), primary_key=True, nullable=False),
    ),
    relevance: float = Field(..., nullable=False)



# Température (°C)
class SensorTemperatureModel(SQLModel, table=True):
    __tablename__ = "sensor_temperature"
    id: int | None = Field(default=None, primary_key=True)
    value: float = Field(..., nullable=False)
    recorded_at: datetime = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False),
    )


# Tension (V)
class SensorVoltageModel(SQLModel, table=True):
    __tablename__ = "sensor_voltage"
    id: int | None = Field(default=None, primary_key=True)
    value: float = Field(..., nullable=False)
    recorded_at: datetime = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False),
    )
