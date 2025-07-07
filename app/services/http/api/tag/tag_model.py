from typing import List
from typing import Optional
from pydantic import BaseModel, Field

class TagsBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    source_address: str = Field(..., min_length=3)
    description: Optional[str] = None

class TagsCreate(TagsBase):
    pass

class TagsUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=255)
    source_address: Optional[str] = Field(default=None, min_length=3)
    description: Optional[str] = None

class Tags(TagsBase):
    id: int

class PaginatedTags(BaseModel):
    data: List[Tags]
    count: int
    offset: int
    limit: int


