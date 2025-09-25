from dataclasses import asdict, dataclass
from datetime import datetime

from dateutil.parser import parse as parse_datetime


@dataclass
class Temperature:
    time: datetime
    sensor_id: int | None
    host: str | None
    source_address: str | None
    temperature: float | None
    event_id: int | None
    relevance: float | None = 1.0

    @staticmethod
    def from_dict(data: dict) -> "Temperature":
        def safe_parse(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return parse_datetime(value)
            return None

        return Temperature(
            time=safe_parse(data["time"]),
            sensor_id=int(data["sensor_id"]) if data.get("sensor_id") is not None else None,
            host=data.get("host"),
            source_address=data.get("source_address"),
            temperature=float(data["temperature"]) if data.get("temperature") is not None else None,
            event_id=int(data["event_id"]) if data.get("event_id") is not None else None,
            relevance=float(data.get("relevance", 1.0)) if data.get("relevance") is not None else 1.0,
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        
        if data["time"]:
            data["time"] = data["time"].isoformat()

        return data