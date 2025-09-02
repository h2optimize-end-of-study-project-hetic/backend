from abc import ABC, abstractmethod

from app.src.domain.entities.sensor import Sensor


class SensorRepository(ABC):
    @abstractmethod
    def create_sensor_data(self, sensor: Sensor) -> Sensor:
        pass

    @abstractmethod
    def paginate_sensors(
        self, cursor: int | None, limit: int
    ) -> tuple[list[Sensor], int, Sensor | None, Sensor | None]:
        pass

    @abstractmethod
    def select_sensors(
        self, offset: int | None = None, limit: int | None = None
    ) -> list[Sensor | None]:
        pass

    @abstractmethod
    def select_sensor_by_id(self, sensor_id: int) -> Sensor:
        pass
