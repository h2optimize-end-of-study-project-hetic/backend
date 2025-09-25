from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class DataRepository(ABC):
    @abstractmethod
    def get_rooms_with_sensor_data(
        self,
        room_ids: list[int] | None = None,
        first_value_date: datetime | None = None,
        smooth_interval_minutes: int = 30
    ) -> list[dict[str, Any]]:
        pass