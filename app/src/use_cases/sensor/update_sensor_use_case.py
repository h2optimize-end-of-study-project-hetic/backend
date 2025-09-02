from app.src.common.exception import NotFoundError, UpdateFailedError
from app.src.domain.interface_repositories.sensor_repository import SensorRepository
from app.src.domain.entities.sensor import Sensor


class UpdateSensorUseCase:
    def __init__(self, sensor_repository: SensorRepository):
        self.sensor_repository = sensor_repository

    def execute(self, sensor_id: int, sensor_data: dict) -> Sensor:
        try:
            updated_sensor = self.sensor_repository.update_sensor(sensor_id, sensor_data)
            if not updated_sensor:
                raise NotFoundError(f"Sensor with ID {sensor_id} not found")
            return updated_sensor
        except NotFoundError:
            raise
        except Exception as e:
            raise UpdateFailedError("Sensor", str(e)) from e
