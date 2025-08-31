import logging
import math
from dataclasses import dataclass

from app.src.domain.entities.group import Group
from app.src.common.utils import decode, encode
from app.src.domain.interface_repositories.group_repository import GroupRepository

logger = logging.getLogger(__name__)

@dataclass
class PaginatedGroup:
    groups: list[Group]
    total: int| None
    chunk_size: int| None
    chunk_count: int | None
    current_cursor: str | None
    first_cursor: str | None
    last_cursor: str | None
    next_cursor: str | None


class GetGroupListUseCase:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    def execute(self, cursor: str | None, limit: int | None = None) -> PaginatedGroup:
        limit = limit or 20

        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, "Group pagination cursor")
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        groups, total, first_group, last_group = self.group_repository.paginate_groups(decoded_cursor, (limit + 1))

        next_group = None
        if len(groups) == (limit + 1):
            next_group = groups.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        first_cursor = {"id": first_group.id} if first_group else None
        last_cursor = {"id": last_group.id} if last_group else None
        next_cursor = {"id": next_group.id} if next_group else None

        return PaginatedGroup(
            groups=groups,
            total=total,
            chunk_size=len(groups),
            chunk_count=chunk_count,
            current_cursor=encode({"id": decoded_cursor}) if decoded_cursor else encode(first_cursor) if first_cursor else None,
            first_cursor=encode(first_cursor) if first_cursor else None,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )
