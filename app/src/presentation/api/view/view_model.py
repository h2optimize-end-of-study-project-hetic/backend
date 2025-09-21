from datetime import datetime
from pydantic import BaseModel

class UserEventViewResponse(BaseModel):
    group: str
    supervisor: str
    room: str
    event: str
    start_at: datetime
    end_at: datetime


class EventsByDateViewResponse(BaseModel):
    room_id: int
    event_id: int
    event_name: str
    description: str
    group_id: int
    group_name: str
    start_at: datetime
    end_at: datetime
    supervisor: str
    member_count: int
