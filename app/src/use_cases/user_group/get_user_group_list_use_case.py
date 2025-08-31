import logging
import math
from dataclasses import dataclass

from app.src.domain.entities.user_group import UserGroup
from app.src.common.utils import decode, encode
from app.src.domain.interface_repositories.user_group_repository import UserGroupRepository

logger = logging.getLogger(__name__)

@dataclass
class PaginatedUserGroup:
    user_groups: list[UserGroup]
    total: int| None
    chunk_size: int| None
    chunk_count: int | None
    current_cursor: str | None
    first_cursor: str | None
    last_cursor: str | None
    next_cursor: str | None


class GetUserGroupListUseCase:
    def __init__(self, user_group_repository: UserGroupRepository):
        self.user_group_repository = user_group_repository

    def execute(self, cursor: str | None, limit: int | None = None) -> PaginatedUserGroup:
        limit = limit or 20

        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, "UserGroup pagination cursor")
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        user_groups, total, first_user_group, last_user_group = self.user_group_repository.paginate_user_groups(decoded_cursor, (limit + 1))

        next_user_group = None
        if len(user_groups) == (limit + 1):
            next_user_group = user_groups.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        first_cursor = {"id": first_user_group.id} if first_user_group else None
        last_cursor = {"id": last_user_group.id} if last_user_group else None
        next_cursor = {"id": next_user_group.id} if next_user_group else None

        return PaginatedUserGroup(
            user_groups=user_groups,
            total=total,
            chunk_size=len(user_groups),
            chunk_count=chunk_count,
            current_cursor=encode({"id": decoded_cursor}) if decoded_cursor else encode(first_cursor) if first_cursor else None,
            first_cursor=encode(first_cursor) if first_cursor else None,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )
