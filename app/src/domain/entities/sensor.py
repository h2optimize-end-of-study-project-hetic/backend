from datetime import datetime
from dataclasses import asdict, dataclass
from dateutil.parser import parse as parse_datetime


@dataclass
class Sensor:
    id: int | None
    sensor_type: str
    value: float
    recorded_at: datetime | None = None

    @staticmethod
    def from_dict(data: dict) -> "Sensor":
        return Sensor(
            id=data.get("id"),
            sensor_type=data["sensor_type"],
            value=data["value"],
            recorded_at=parse_datetime(data["recorded_at"]) if data.get("recorded_at") else None,
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        if data["recorded_at"]:
            data["recorded_at"] = data["recorded_at"].isoformat()
        return data
