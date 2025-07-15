from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass, asdict
from dateutil.parser import parse as parse_datetime


@dataclass
class Tag:
    id: Optional[int]
    name: str
    description: Optional[str]
    source_address: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime] = None

    @staticmethod
    def from_dict(data: Dict) -> "Tag":
        def safe_parse(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return parse_datetime(value)
            return None

        return Tag(
            id=data.get("id"),
            name=data["name"],
            description=data.get("description"),
            source_address=data["source_address"],
            created_at=safe_parse(data.get("created_at")),
            updated_at=safe_parse(data.get("updated_at")),
        )

    def to_dict(self) -> Dict:
        data = asdict(self)
        for field in ["created_at", "updated_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data

