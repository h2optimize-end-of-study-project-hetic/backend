import logging
from sqlalchemy import func
from typing import List, Optional
from sqlmodel import Session, select

from app.src.common.exception import CreationFailedException, NotFoundException
from app.src.domain.entities.tag import Tag
from app.src.infrastructure.db.models.tag_model import TagModel
from app.src.domain.interface_repositories.tag_repository import TagRepository

class SQLTagRepository(TagRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_tag(self, tag: Tag) -> Tag:
        tag_model = TagModel(
            name=tag.name,
            description=tag.description,
            source_address=tag.source_address,
        )
        try:
            self.session.add(tag_model)
            self.session.commit()
            self.session.refresh(tag_model)
        except Exception as e:
            logging.error(e)
            self.session.rollback()
            raise CreationFailedException("Tag", str(e)) from e
        
        return Tag.from_dict(tag_model.model_dump())
    

    def select_tags(self, cursor: Optional[int] = None, limit: Optional[int] = None) -> List[Tag]:
        statement = select(TagModel).order_by(TagModel.id)
        if cursor:
            statement = statement.where(TagModel.id >= cursor)
        statement = statement.limit(limit)

        results = self.session.exec(statement).all()
        return [Tag(**tag.model_dump()) for tag in results]
    

    def count_all_tags(self) -> int:
        total = self.session.exec(select(func.count()).select_from(TagModel)).one()
        return total
    
    def get_tag_by_position(self, position: int) -> Optional[Tag]:
        if position >= 0:
            statement = (
                select(TagModel)
                .order_by(TagModel.id.asc())
                .offset(position)
                .limit(1)
            )
        else:
            statement = (
                select(TagModel)
                .order_by(TagModel.id.desc())
                .offset(abs(position) - 1)
                .limit(1)
            )

        result = self.session.exec(statement).first()
        return Tag(**result.model_dump()) if result else None
    

    def select_tag_by_id(self, tag_id: int) -> Optional[Tag]:
        statement = select(TagModel).where(TagModel.id == tag_id)
        result = self.session.exec(statement).first()

        if not result:
            raise NotFoundException("Tag", tag_id)
        
        return Tag(**result.model_dump())


    def select_tag_by_src_address(self, tag_src_address: str) -> Tag:
        statement = select(TagModel).where(TagModel.source_address == tag_src_address)
        result = self.session.exec(statement).first()

        if not result:
            raise NotFoundException("Tag", tag_src_address)
        
        return Tag(**result.model_dump())


    def update_tag(self, tag_id: int) -> Tag:
        pass

    def delete_tag(self, tag_id: int) -> bool:
        pass