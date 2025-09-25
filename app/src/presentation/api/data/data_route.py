import logging
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.src.domain.entities.role import Role
from app.src.domain.entities.user import User
from app.src.presentation.api.data.data_model import RoomSensorDataModel, RoomTagModel, RoomsSensorDataResponseModel, SensorDataStatsModel, SingleRoomSensorDataResponseModel, TagInfoModel
from app.src.presentation.api.secure_ressources import secure_ressources
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.presentation.api.common.errors import OpenApiErrorResponseConfig, generate_responses

from app.src.presentation.dependencies import (
    get_rooms_sensor_data_use_case,
    get_single_room_sensor_data_use_case
)


from app.src.common.exception import NotFoundError
from app.src.use_cases.data.get_rooms_sensor_data_use_case import GetRoomsSensorDataUseCase
from app.src.use_cases.data.get_single_room_sensor_use_case import GetSingleRoomSensorDataUseCase

room_not_found = OpenApiErrorResponseConfig(
    code=404, 
    description="Room not found", 
    detail="Room with ID '123' not found"
)
invalid_params = OpenApiErrorResponseConfig(
    code=400, 
    description="Invalid parameters", 
    detail="Invalid smooth interval or date format"
)
unexpected_error = OpenApiErrorResponseConfig(
    code=500, 
    description="Unexpected error", 
    detail="Internal server error"
)

logger = logging.getLogger(__name__)

data_router = APIRouter(
    prefix=f"/{OpenApiTags.data.value}", 
    tags=["data"]
)


@data_router.get(
    "/rooms",
    summary="Récupérer les données de capteurs pour plusieurs pièces",
    response_model=RoomsSensorDataResponseModel,
    response_description="Données agrégées et lissées des capteurs pour les pièces",
    responses=generate_responses([invalid_params, unexpected_error]),
    deprecated=False,
)
async def get_rooms_sensor_data(
    use_case: Annotated[GetRoomsSensorDataUseCase, Depends(get_rooms_sensor_data_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    room_ids: list[int] | None = Query(
        None,
        description="Liste des IDs des pièces (ex: room_ids=1&room_ids=2). Si vide, toutes les pièces."
    ),
    first_value_date: datetime | None = Query(
        None,
        description="Date de début pour filtrer les données (format: 2024-01-01T00:00:00)"
    ),
    smooth_interval_minutes: int = Query(
        30,
        ge=1,
        le=1440,
        description="Intervalle de lissage en minutes (1-1440, défaut: 30)"
    ),
):
    """
    Récupère les données de capteurs agrégées et lissées pour plusieurs rooms.
    
    **Fonctionnalités Avancées:**
    
    **Lissage des valeurs:**
    - Après lissage (30min): `0:30→79, 1:00→60` (interpolation linéaire)
    
    **Agrégation des valeurs des balises:**
    - Moyenne des valeurs des balises dans une pièces

    **Paramètres:**
    - **room_ids**: IDs des rooms (optionnel, toutes si omis)
    - **first_value_date**: Date de début
    - **smooth_interval_minutes**: Lissage en minutes (1-1440)
    
    **Exemple URL:**
    `/room/sensor-data/rooms?room_ids=1&room_ids=2&first_value_date=2024-01-01T00:00:00&smooth_interval_minutes=60`
    """
    try:
        result = use_case.execute(
            room_ids=room_ids,
            first_value_date=first_value_date,
            smooth_interval_minutes=smooth_interval_minutes
        )

        rooms_data = []
        for room_data in result.rooms_data:
            tags_models = []
            for tag_data in room_data.get("tags", []):
                tag_model = RoomTagModel(
                    id=tag_data["id"],
                    tag=TagInfoModel(**tag_data["tag"]),
                    start_at=tag_data["start_at"],
                    end_at=tag_data["end_at"],
                    created_at=tag_data["created_at"],
                    updated_at=tag_data["updated_at"]
                )
                tags_models.append(tag_model)

            sensor_data = {}
            for sensor_type in ["temperature", "humidity", "pressure"]:
                if sensor_type in room_data:
                    sensor_data[sensor_type] = SensorDataStatsModel(**room_data[sensor_type])

            room_model = RoomSensorDataModel(
                id=room_data["id"],
                name=room_data["name"],
                description=room_data["description"],
                floor=room_data["floor"],
                building_id=room_data["building_id"],
                area=room_data["area"],
                capacity=room_data["capacity"],
                start_at=room_data["start_at"],
                end_at=room_data["end_at"],
                created_at=room_data["created_at"],
                updated_at=room_data["updated_at"],
                tags=tags_models,
                **sensor_data
            )
            rooms_data.append(room_model)

        return RoomsSensorDataResponseModel(
            data=rooms_data,
            total_rooms=result.total_rooms
        )

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Paramètres invalides: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Paramètres invalides: {e!s}"
        ) from e
    except Exception as e:
        logger.error(f"Erreur inattendue dans get_rooms_sensor_data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        ) from e


@data_router.get(
    "/room/{room_id}",
    summary="Récupérer les données de capteurs pour une pièce",
    response_model=SingleRoomSensorDataResponseModel,
    response_description="Données agrégées et lissées des capteurs pour la pièce spécifiée",
    responses=generate_responses([room_not_found, invalid_params, unexpected_error]),
    deprecated=False,
)
async def get_single_room_sensor_data(
    use_case: Annotated[GetSingleRoomSensorDataUseCase, Depends(get_single_room_sensor_data_use_case)],
    user: Annotated[User, Depends(secure_ressources([Role.staff, Role.technician]))],
    room_id: int = Path(..., ge=1, description="ID de la pièce (entier positif)"),
    first_value_date: datetime | None = Query(
        None,
        description="Date de début pour filtrer les données (format: 2024-01-01T00:00:00)"
    ),
    smooth_interval_minutes: int = Query(
        30,
        ge=1,
        le=1440,
        description="Intervalle de lissage en minutes (1-1440, défaut: 30)"
    ),
):
    """
    Récupère les données de capteurs agrégées et lissées pour une pièce spécifique.
    
    **Paramètres:**
    - **room_id**: ID de la pièce (obligatoire, ≥ 1)
    - **first_value_date**: Date de début
    - **smooth_interval_minutes**: Lissage en minutes (1-1440)
    """
    try:

        result = use_case.execute(
            room_id=room_id,
            first_value_date=first_value_date,
            smooth_interval_minutes=smooth_interval_minutes
        )

        tags_models = []
        for tag_data in result.get("tags", []):
            tag_model = RoomTagModel(
                id=tag_data["id"],
                tag=TagInfoModel(**tag_data["tag"]),
                start_at=tag_data["start_at"],
                end_at=tag_data["end_at"],
                created_at=tag_data["created_at"],
                updated_at=tag_data["updated_at"]
            )
            tags_models.append(tag_model)

        sensor_data = {}
        for sensor_type in ["temperature", "humidity", "pressure"]:
            if sensor_type in result:
                sensor_data[sensor_type] = SensorDataStatsModel(**result[sensor_type])

        room_model = RoomSensorDataModel(
            id=result["id"],
            name=result["name"],
            description=result["description"],
            floor=result["floor"],
            building_id=result["building_id"],
            area=result["area"],
            capacity=result["capacity"],
            start_at=result["start_at"],
            end_at=result["end_at"],
            created_at=result["created_at"],
            updated_at=result["updated_at"],
            tags=tags_models,
            **sensor_data
        )

        return SingleRoomSensorDataResponseModel(data=room_model)

    except NotFoundError as e:
        logger.error(f"Room {room_id} non trouvée: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Paramètres invalides: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Paramètres invalides: {e!s}"
        ) from e
    except Exception as e:
        logger.error(f"Erreur inattendue dans get_single_room_sensor_data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        ) from e