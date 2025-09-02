from app.src.common.exception import CreationFailedError
from app.src.domain.entities.sensor import Sensor
from app.src.domain.interface_repositories.sensor_repository import SensorRepository


class CreateSensorUseCase:
    def __init__(self, sensor_repository: SensorRepository):
        self.sensor_repository = sensor_repository

    def execute(self, sensor: Sensor) -> Sensor:
        try:
            new_sensor = self.sensor_repository.create_sensor_data(sensor)
            if not new_sensor:
                raise CreationFailedError("Sensor", "Failed to create sensor entry")
            return new_sensor
        except Exception as e:
            raise CreationFailedError("Sensor", str(e)) from e
