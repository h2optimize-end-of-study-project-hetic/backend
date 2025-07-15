from sqlmodel import Session, select
from typing import List, Optional

from app.src.domain.entities.room import Room
from app.src.domain.interface_repositories.room_repository import RoomRepository

class SQLRoomRepository(RoomRepository):
    def __init__(self, session: Session):
        self.session = session

    def select_room_by_id(self, room_id: int) -> Room:
        pass
