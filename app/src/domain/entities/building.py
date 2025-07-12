from datetime import datetime
from typing import Optional, Any, Dict
from dataclasses import dataclass, asdict
from dateutil.parser import parse as parse_datetime

@dataclass
class Building:
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    room_count: Optional[int]    
    created_at: Optional[datetime]
    updated_at: Optional[datetime] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Building":
        return Building(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            room_count=data.get("room_count"),
            created_at=parse_datetime(data["created_at"]) if data.get("created_at") else None,
            updated_at=parse_datetime(data["updated_at"]) if data.get("updated_at") else None,
        )

    def to_dict(self) -> Dict:
        data = asdict(self)
        for field in ["created_at", "updated_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data
