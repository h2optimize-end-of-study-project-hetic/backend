import logging
from dataclasses import dataclass
from typing import Literal

from app.src.domain.entities.room import Room
from app.src.domain.interface_repositories.room_repository import RoomRepository

logger = logging.getLogger(__name__)


@dataclass
class RoomListResult:
    rooms: list[Room]
    total: int
    offset: int | None
    limit: int
    order_by: str
    order_direction: Literal["asc", "desc"]


class GetRoomListUseCase:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository
    
    def execute(self, offset: int | None = None, limit: int | None = None) -> RoomListResult:
        rooms = self.room_repository.select_rooms(offset, limit)
        total = self.room_repository.count_all_rooms()

        return RoomListResult(
            rooms=rooms,
            total=total,
            offset=offset,
            limit=limit,
            order_by="created_at",
            order_direction="asc"
        )