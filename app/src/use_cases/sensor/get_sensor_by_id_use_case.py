from app.src.common.exception import NotFoundError
from app.src.domain.interface_repositories.sensor_repository import SensorRepository
from app.src.domain.entities.sensor import Sensor


class GetSensorByIdUseCase:
    def __init__(self, sensor_repository: SensorRepository):
        self.sensor_repository = sensor_repository

    def execute(self, sensor_id: int) -> Sensor:
        sensor = self.sensor_repository.select_sensor_by_id(sensor_id)
        if sensor is None:
            raise NotFoundError(f"Sensor with ID {sensor_id} not found")
        return sensor
