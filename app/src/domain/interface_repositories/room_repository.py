from typing import List, Optional
from abc import ABC, abstractmethod

from app.src.domain.entities.room import Room

class RoomRepository(ABC):

    @abstractmethod
    def select_room_by_id(self, room_id: int) -> Room:
        pass
