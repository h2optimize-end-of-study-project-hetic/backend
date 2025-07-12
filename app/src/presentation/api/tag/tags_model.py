from typing import List
from typing import Optional
from pydantic import BaseModel, Field

class TagsBaseModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    source_address: str = Field(..., min_length=3)
    description: Optional[str] = None

class TagsCreateModel(TagsBaseModel):
    pass

class TagsUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=255)
    source_address: Optional[str] = Field(default=None, min_length=3)
    description: Optional[str] = None

class TagsModel(TagsBaseModel):
    id: int

class PaginatedTagsModel(BaseModel):
    data: List[TagsModel]
    count: int
    offset: int
    limit: int