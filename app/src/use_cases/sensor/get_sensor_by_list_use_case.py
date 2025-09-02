import math
import logging
from dataclasses import dataclass
from app.src.domain.entities.sensor import Sensor
from app.src.common.utils import decode, encode
from app.src.domain.interface_repositories.sensor_repository import SensorRepository

logger = logging.getLogger(__name__)


@dataclass
class PaginatedSensor:
    sensors: list[Sensor]
    total: int | None
    chunk_size: int | None
    chunk_count: int | None
    current_cursor: str | None
    first_cursor: str | None
    last_cursor: str | None
    next_cursor: str | None


class GetSensorListUseCase:
    def __init__(self, sensor_repository: SensorRepository):
        self.sensor_repository = sensor_repository

    def execute(self, cursor: str | None, limit: int | None = None) -> PaginatedSensor:
        limit = limit or 20

        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, "Sensor pagination cursor")
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        sensors, total, first_sensor, last_sensor = self.sensor_repository.paginate_sensors(
            decoded_cursor, (limit + 1)
        )

        next_sensor = None
        if len(sensors) == (limit + 1):
            next_sensor = sensors.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        first_cursor = {"id": first_sensor.id} if first_sensor else None
        last_cursor = {"id": last_sensor.id} if last_sensor else None
        next_cursor = {"id": next_sensor.id} if next_sensor else None

        return PaginatedSensor(
            sensors=sensors,
            total=total,
            chunk_size=len(sensors),
            chunk_count=chunk_count,
            current_cursor=encode({"id": decoded_cursor})
            if decoded_cursor
            else encode(first_cursor)
            if first_cursor
            else None,
            first_cursor=encode(first_cursor) if first_cursor else None,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )
