
import logging
from datetime import datetime
from typing import Any

from app.src.domain.interface_repositories.data_repository import DataRepository
from app.src.domain.interface_repositories.room_repository import RoomRepository
from app.src.common.exception import NotFoundError
from app.src.use_cases.data.get_rooms_sensor_data_use_case import GetRoomsSensorDataUseCase

logger = logging.getLogger(__name__)


class GetSingleRoomSensorDataUseCase:
    def __init__(
        self,
        data_repository: DataRepository,
        room_repository: RoomRepository
    ):
        self.data_repository = data_repository
        self.room_repository = room_repository

    def execute(
        self,
        room_id: int,
        first_value_date: datetime | None = None,
        smooth_interval_minutes: int = 30
    ) -> dict[str, Any]:
        try:
            self.room_repository.select_room_by_id(room_id)

            get_multiple_use_case = GetRoomsSensorDataUseCase(
                self.data_repository,
                self.room_repository
            )

            result = get_multiple_use_case.execute(
                room_ids=[room_id],
                first_value_date=first_value_date,
                smooth_interval_minutes=smooth_interval_minutes
            )

            if not result.rooms_data:
                raise NotFoundError("Room", room_id)

            return result.rooms_data[0]

        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error get rooms data {room_id}: {e}")
            raise