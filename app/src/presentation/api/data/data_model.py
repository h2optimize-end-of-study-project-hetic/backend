from datetime import datetime
from pydantic import BaseModel, Field


class TagInfoModel(BaseModel):
    id: int = Field(..., description="ID du balise")
    name: str = Field(..., description="Nom du balise")
    source_address: str = Field(..., description="Adresse source du capteur")
    description: str | None = Field(None, description="Description du balise")
    created_at: str | None = Field(None, description="Date de création")
    updated_at: str | None = Field(None, description="Date de mise à jour")


class RoomTagModel(BaseModel):
    id: int = Field(..., description="ID de la relation room-tag")
    tag: TagInfoModel = Field(..., description="Informations du balise")
    start_at: str | None = Field(None, description="Date de début d'activité")
    end_at: str | None = Field(None, description="Date de fin d'activité")
    created_at: str | None = Field(None, description="Date de création de la relation")
    updated_at: str | None = Field(None, description="Date de mise à jour de la relation")


class SensorDataStatsModel(BaseModel):
    min: float | None = Field(None, description="Valeur minimale")
    max: float | None = Field(None, description="Valeur maximale")
    average: float | None = Field(None, description="Valeur moyenne")
    nombre_values: int = Field(0, description="Nombre de valeurs")
    data: list[list[float]] = Field(
        default_factory=list, 
        description="Données au format [[timestamp_ms, valeur]]"
    )


class RoomSensorDataModel(BaseModel):
    id: int = Field(..., description="ID de la piece")
    name: str = Field(..., description="Nom de la piece")
    description: str | None = Field(None, description="Description de la piece")
    floor: int | None = Field(None, description="Étage de la piece")
    building_id: int = Field(..., description="ID du bâtiment")
    area: float | None = Field(None, description="Surface de la piece")
    capacity: int | None = Field(None, description="Capacité de la pieces")
    start_at: str | None = Field(None, description="Date de début de validité")
    end_at: str | None = Field(None, description="Date de fin de validité")
    created_at: str | None = Field(None, description="Date de création")
    updated_at: str | None = Field(None, description="Date de mise à jour")
    tags: list[RoomTagModel] = Field(default_factory=list, description="Balises associés à la pieces")
    
    temperature: SensorDataStatsModel | None = Field(None, description="Données de température")
    humidity: SensorDataStatsModel | None = Field(None, description="Données d'humidité")
    pressure: SensorDataStatsModel | None = Field(None, description="Données de pression atmosphérique")


class RoomsSensorDataResponseModel(BaseModel):
    data: list[RoomSensorDataModel] = Field(..., description="Liste des pieces avec données capteurs")
    total_rooms: int = Field(..., description="Nombre total de pieces retournées")


class SingleRoomSensorDataResponseModel(BaseModel):
    data: RoomSensorDataModel = Field(..., description="Données de la piece avec capteurs")


class SensorDataQueryParams(BaseModel):
    room_ids: list[int] | None = Field(
        None, 
        description="Liste des IDs des pieces (optionnel, toutes si vide)"
    )
    first_value_date: datetime | None = Field(
        None, 
        description="Date de début pour filtrer les données"
    )
    smooth_interval_minutes: int = Field(
        30, 
        ge=1, 
        le=1440, 
        description="Intervalle de lissage en minutes (1-1440, défaut: 30)"
    )
