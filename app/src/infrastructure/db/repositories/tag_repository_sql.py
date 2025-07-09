from sqlmodel import Session, select
from typing import List, Optional

from app.src.domain.entities.tag import Tag
from app.src.infrastructure.db.models.tag_model import TagModel
from app.src.domain.interface_repositories.tag_repository import TagRepository

class SQLTagRepository(TagRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_tag(self, tag: Tag) -> Tag:
        pass

    def select_tags(self, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Optional[Tag]]:
        pass

    def select_tag_by_id(self, tag_id: int) -> Tag:
        statement = select(TagModel).where(TagModel.id == tag_id)
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError(f"Tag with ID {tag_id} not found")
        
        return Tag(
            id=result.id,
            name=result.name,
            description=result.description,
            source_address=result.source_address,
            created_at=result.created_at,
            updated_at=result.updated_at,
        )


    def select_tag_by_src_address(self, tag_src_address: str) -> Tag:
        pass

    def update_tag(self, tag_id: int) -> Tag:
        pass

    def delete_tag(self, tag_id: int) -> bool:
        pass