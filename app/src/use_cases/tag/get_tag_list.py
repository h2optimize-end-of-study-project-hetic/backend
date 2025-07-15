from dataclasses import dataclass
import math
from typing import List, Optional

from app.src.domain.entities.tag import Tag
from app.src.common.utils import encode, decode
from app.src.domain.interface_repositories.tag_repository import TagRepository

@dataclass
class PaginatedTag:
    tags: List[Tag]
    total: int
    chunk_size: int
    chunk_count: int
    current_cursor: Optional[str]
    first_cursor: Optional[str]
    last_cursor: Optional[str]
    next_cursor: Optional[str]

class GetTagListUseCase:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def execute(self, cursor: Optional[str], limit: Optional[int] = None) -> PaginatedTag:
        limit = limit or 20

        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, 'Tag pagination cursor')
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        tags = self.tag_repository.select_tags(decoded_cursor, (limit + 1))

        next_tag = None
        if len(tags) == (limit + 1):
            next_tag = tags.pop(-1)

        total = self.tag_repository.count_all_tags()
        chunk_count = math.ceil(total / limit) if limit else 1
        
        first_tag:Optional[Tag] = self.tag_repository.get_tag_by_position(0)
        last_tag:Optional[Tag] = self.tag_repository.get_tag_by_position(max((-1 * limit), (-1 * total)))

        first_cursor = {"id": first_tag.id} if first_tag else None
        last_cursor = {"id": last_tag.id} if last_tag else None
        next_cursor = {"id": next_tag.id} if next_tag else None

        return PaginatedTag(
            tags=tags,
            total=total,
            chunk_size=len(tags),
            chunk_count=chunk_count,
            current_cursor=cursor if cursor else encode(first_cursor) if first_cursor else None,
            first_cursor=encode(first_cursor)if first_cursor else None ,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )