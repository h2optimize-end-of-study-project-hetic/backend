from datetime import datetime
from dataclasses import asdict, dataclass
from dateutil.parser import parse as parse_datetime
from app.src.domain.entities.role import Role


@dataclass
class User:
    id: int | None
    email: str
    password: str
    firstname: str
    lastname: str
    salt: str | None
    secret_2fa: str | None
    phone_number: str | None
    created_at: datetime | None
    role: Role = Role.guest.value
    is_active: bool = True
    is_delete: bool = False
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    @staticmethod
    def from_dict(data: dict) -> "User":
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

    def to_dict(self) -> dict:
        data = asdict(self)
        data["role"] = self.role.value if hasattr(self.role, "value") else self.role
        for field in ["created_at", "updated_at", "deleted_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data
