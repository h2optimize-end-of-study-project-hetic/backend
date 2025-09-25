import logging
from datetime import datetime
from dataclasses import dataclass
from typing import Any

from app.src.domain.interface_repositories.data_repository import DataRepository
from app.src.domain.interface_repositories.room_repository import RoomRepository
from app.src.common.exception import NotFoundError

logger = logging.getLogger(__name__)


@dataclass
class GetRoomSensorDataResult:
    rooms_data: list[dict[str, Any]]
    total_rooms: int


class GetRoomsSensorDataUseCase:
    def __init__(
        self,
        data_repository: DataRepository,
        room_repository: RoomRepository
    ):
        self.data_repository = data_repository
        self.room_repository = room_repository

    def execute(
        self,
        room_ids: list[int] | None = None,
        first_value_date: datetime | None = None,
        smooth_interval_minutes: int = 30
    ) -> GetRoomSensorDataResult:

        try:
            if smooth_interval_minutes <= 0:
                smooth_interval_minutes = 30
            elif smooth_interval_minutes > 1440:  # Max 24h
                smooth_interval_minutes = 1440

            validated_room_ids = self._validate_room_ids(room_ids) if room_ids else None

            rooms_data = self.data_repository.get_rooms_with_sensor_data(
                room_ids=validated_room_ids,
                first_value_date=first_value_date,
                smooth_interval_minutes=smooth_interval_minutes
            )

            processed_rooms = []
            for room_data in rooms_data:
                processed_room = self._format_room_data(room_data)
                processed_rooms.append(processed_room)

            processed_rooms.sort(key=lambda x: x["id"])

            return GetRoomSensorDataResult(
                rooms_data=processed_rooms,
                total_rooms=len(processed_rooms)
            )

        except Exception as e:
            logger.error(f"Error GetRoomsSensorData: {e}")
            raise

    def _validate_room_ids(self, room_ids: list[int]) -> list[int]:

        validated_ids = []
        for room_id in room_ids:
            try:
                self.room_repository.select_room_by_id(room_id)
                validated_ids.append(room_id)
            except NotFoundError:
                logger.warning(f"Room {room_id} not found")
                continue
        
        return validated_ids

    def _format_room_data(self, room_data: dict[str, Any]) -> dict[str, Any]:
        formatted = {
            "id": room_data.get("id"),
            "name": room_data.get("name"),
            "description": room_data.get("description"),
            "floor": room_data.get("floor"),
            "building_id": room_data.get("building_id"),
            "area": room_data.get("area"),
            "capacity": room_data.get("capacity"),
            "start_at": room_data.get("start_at").isoformat() if room_data.get("start_at") else None,
            "end_at": room_data.get("end_at").isoformat() if room_data.get("end_at") else None,
            "created_at": room_data.get("created_at").isoformat() if room_data.get("created_at") else None,
            "updated_at": room_data.get("updated_at").isoformat() if room_data.get("updated_at") else None,
            "tags": []
        }

        for tag_info in room_data.get("tags", []):
            formatted_tag = {
                "id": tag_info["id"],
                "tag": {
                    "id": tag_info["tag"].id,
                    "name": tag_info["tag"].name,
                    "source_address": tag_info["tag"].source_address,
                    "description": tag_info["tag"].description,
                    "created_at": tag_info["tag"].created_at.isoformat() if tag_info["tag"].created_at else None,
                    "updated_at": tag_info["tag"].updated_at.isoformat() if tag_info["tag"].updated_at else None
                },
                "start_at": tag_info["start_at"].isoformat() if tag_info["start_at"] else None,
                "end_at": tag_info["end_at"].isoformat() if tag_info["end_at"] else None,
                "created_at": tag_info["created_at"].isoformat() if tag_info["created_at"] else None,
                "updated_at": tag_info["updated_at"].isoformat() if tag_info["updated_at"] else None
            }
            formatted["tags"].append(formatted_tag)

        sensor_types = ["temperature", "humidity", "pressure"]
        for sensor_type in sensor_types:
            if sensor_type in room_data:
                sensor_data = room_data[sensor_type]
                formatted[sensor_type] = {
                    "min": sensor_data.get("min"),
                    "max": sensor_data.get("max"),
                    "average": sensor_data.get("average"),
                    "nombre_values": sensor_data.get("nombre_values", 0),
                    "data": sensor_data.get("data", [])
                }

        return formatted

