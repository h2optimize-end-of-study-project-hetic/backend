from datetime import datetime
from dataclasses import asdict, dataclass

from dateutil.parser import parse as parse_datetime

@dataclass
class UserGroup:
    group_id: int | None
    user_id: int | None
    created_at: datetime | None
    updated_at: datetime | None = None

    @staticmethod
    def from_dict(data: dict) -> "UserGroup":
        def safe_parse(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return parse_datetime(value)
            return None

        return UserGroup(
            group_id=data.get("group_id"),
            user_id=data.get("user_id"),
            created_at=safe_parse(data.get("created_at")),
            updated_at=safe_parse(data.get("updated_at")),
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        for field in ["created_at", "updated_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data
