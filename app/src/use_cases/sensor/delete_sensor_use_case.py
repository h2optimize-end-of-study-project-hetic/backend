from app.src.common.exception import NotFoundError, ForeignKeyConstraintError
from sqlalchemy.exc import IntegrityError
from app.src.domain.interface_repositories.sensor_repository import SensorRepository


class DeleteSensorUseCase:
    def __init__(self, sensor_repository: SensorRepository):
        self.sensor_repository = sensor_repository

    def execute(self, sensor_id: int):
        try:
            self.sensor_repository.delete_sensor(sensor_id)
        except ValueError:
            raise NotFoundError(f"Sensor with ID {sensor_id} not found")
        except IntegrityError as e:
            if hasattr(e.orig, "pgcode") and e.orig.pgcode == "23503":
                raise ForeignKeyConstraintError(f"Sensor is still referenced: {str(e.orig)}") from e
            raise
