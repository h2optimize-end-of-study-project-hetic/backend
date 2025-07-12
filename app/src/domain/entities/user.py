from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass, asdict
from dateutil.parser import parse as parse_datetime

from app.src.domain.entities.role import Role

@dataclass
class User:
    id: Optional[int]
    email: str
    password: str
    salt: str
    secret_2fa: Optional[str]
    role: Role = Role.GUEST
    firstname: str
    lastname: str
    phone_number: Optional[str]
    is_active: bool = True
    is_delete: bool = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @staticmethod
    def from_dict(data: Dict) -> "User":
        return User(
            id=data.get("id"),
            email=data["email"],
            password=data["password"],
            salt=data["salt"],
            secret_2fa=data.get("secret_2fa"),
            role=Role(data["role"]),
            firstname=data["firstname"],
            lastname=data["lastname"],
            phone_number=data.get("phone_number"),
            is_active=data.get("is_active", True),
            is_delete=data.get("is_delete", False),
            created_at=parse_datetime(data["created_at"]) if data.get("created_at") else None,
            updated_at=parse_datetime(data["updated_at"]) if data.get("updated_at") else None,
            deleted_at=parse_datetime(data["deleted_at"]) if data.get("deleted_at") else None,

        )

    def to_dict(self) -> Dict:
        data = asdict(self)
        data["role"] = self.role.value
        for field in ["created_at", "updated_at", "deleted_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data



