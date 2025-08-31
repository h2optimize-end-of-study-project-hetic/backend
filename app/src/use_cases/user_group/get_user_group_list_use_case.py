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

        decoded_cursor: tuple[int,int] | None = None
        if cursor:
            decoded_data = decode(cursor, "UserGroup pagination cursor")
            if decoded_data and "user_id" in decoded_data and "group_id" in decoded_data:
                decoded_cursor = (decoded_data["user_id"], decoded_data["group_id"])

        user_groups, total, first_user_group, last_user_group = self.user_group_repository.paginate_user_groups(
            decoded_cursor, limit + 1
        )

        next_user_group: UserGroup | None = None
        if len(user_groups) == (limit + 1):
            next_user_group = user_groups.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        # Génération des cursors composite
        first_cursor = encode({"user_id": first_user_group.user_id, "group_id": first_user_group.group_id}) if first_user_group else None
        last_cursor  = encode({"user_id": last_user_group.user_id, "group_id": last_user_group.group_id}) if last_user_group else None
        next_cursor  = encode({"user_id": next_user_group.user_id, "group_id": next_user_group.group_id}) if next_user_group else None
        current_cursor = encode({"user_id": decoded_cursor[0], "group_id": decoded_cursor[1]}) if decoded_cursor else first_cursor

        return PaginatedUserGroup(
            user_groups=user_groups,
            total=total,
            chunk_size=len(user_groups),
            chunk_count=chunk_count,
            current_cursor=current_cursor,
            first_cursor=first_cursor,
            last_cursor=last_cursor,
            next_cursor=next_cursor,
        )
