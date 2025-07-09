from datetime import datetime
from typing import Optional, Any, Dict
from dataclasses import dataclass, asdict

@dataclass
class Tag:
    id: Optional[int]
    name: str
    description: Optional[str]
    source_address: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Tag":
        return Tag(
            id=data.get("id"),
            name=data["name"],
            description=data.get("description"),
            source_address=data["source_address"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
