from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Tag:
    id: Optional[int] = None
    name: str = ""
    source_address: str = ""
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
