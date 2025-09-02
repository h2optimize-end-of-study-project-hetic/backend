from datetime import datetime
from pydantic import BaseModel

class UserEventViewResponse(BaseModel):
    group: str
    supervisor: str
    room: str
    event: str
    start_at: datetime
    end_at: datetime
