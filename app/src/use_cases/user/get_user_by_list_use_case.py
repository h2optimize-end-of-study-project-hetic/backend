import logging
import math
from dataclasses import dataclass
from app.src.domain.entities.user import User
from app.src.common.utils import decode, encode
from app.src.domain.interface_repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)

@dataclass
class PaginatedUser:
    users: list[User]
    total: int | None
    chunk_size: int | None
    chunk_count: int | None
    current_cursor: str | None
    first_cursor: str | None
    last_cursor: str | None
    next_cursor: str | None

class GetUserListUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, cursor: str | None, limit: int | None = None) -> PaginatedUser:
        limit = limit or 20

        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, "User pagination cursor")
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        users, total, first_user, last_user = self.user_repository.paginate_users(decoded_cursor, (limit + 1))

        next_user = None
        if len(users) == (limit + 1):
            next_user = users.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        first_cursor = {"id": first_user.id} if first_user else None
        last_cursor = {"id": last_user.id} if last_user else None
        next_cursor = {"id": next_user.id} if next_user else None

        return PaginatedUser(
            users=users,
            total=total,
            chunk_size=len(users),
            chunk_count=chunk_count,
            current_cursor=encode({"id": decoded_cursor}) if decoded_cursor else encode(first_cursor) if first_cursor else None,
            first_cursor=encode(first_cursor) if first_cursor else None,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )