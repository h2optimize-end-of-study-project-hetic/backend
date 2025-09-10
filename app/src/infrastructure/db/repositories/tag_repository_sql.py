from datetime import datetime
import logging

from psycopg2 import errors
from sqlalchemy import func
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.tag import Tag
from app.src.infrastructure.db.models.room_tag_model import RoomTagModel
from app.src.infrastructure.db.models.tag_model import TagModel
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.common.exception import (
    AlreadyExistsError,
    CheckConstraintError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

logger = logging.getLogger(__name__)


class SQLTagRepository(TagRepository):
    def __init__(self, session: Session):
        self.session = session


    def create_tag(self, tag: Tag) -> Tag:
        try:
            tag_model = TagModel(
                name=tag.name,
                description=tag.description,
                source_address=tag.source_address,
            )
            self.session.add(tag_model)
            self.session.flush()
            self.session.commit()
            self.session.refresh(tag_model)
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.UniqueViolation):
                raise AlreadyExistsError("Tag", "source_address", tag_model.source_address) from e
            logger.error(e)
            raise CreationFailedError("Tag", "Integrity error") from e
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise CreationFailedError("Tag", str(e)) from e

        return Tag.from_dict(tag_model.model_dump())


    def paginate_tags(self, cursor: int | None, limit: int, with_rooms: bool = False) -> tuple[list[Tag], int, Tag | None, Tag | None]:       
        tags = self.select_tags(cursor, limit, with_rooms)
        total = self.count_all_tags()
        first_tag = self.get_tag_by_position(0)
        last_page_offset = (
            (total // (limit - 1)) * (limit - 1)
            if total % (limit - 1) != 0
            else ((total // (limit - 1)) - 1) * (limit - 1)
        )

        last_tag = self.get_tag_by_position(last_page_offset)

        return tags, total, first_tag, last_tag


    def select_tags(self, cursor: int | None, limit: int, with_rooms: bool = False) -> list[Tag]:
        statement = select(TagModel).order_by(TagModel.id)
        if cursor:
            statement = statement.where(TagModel.id >= cursor)
        statement = statement.limit(limit)

        results = self.session.exec(statement).all()

        if with_rooms:
            return [
                Tag(
                    **tag.model_dump(),
                    rooms=[
                        {
                            **room_tag.model_dump(),
                            "room": {
                                **room_tag.room.model_dump(),
                                "building": room_tag.room.building.model_dump()
                                if room_tag.room and room_tag.room.building
                                else None,
                            },
                        }
                        for room_tag in tag.room_tags
                    ],
                )
                for tag in results
            ]
        else:
            return [Tag(**tag.model_dump()) for tag in results]



    def count_all_tags(self) -> int:
        total = self.session.exec(select(func.count()).select_from(TagModel)).one()
        return total


    def get_tag_by_position(self, position: int) -> Tag | None:
        if position >= 0:
            statement = select(TagModel).order_by(TagModel.id.asc()).offset(position).limit(1)
        else:
            statement = select(TagModel).order_by(TagModel.id.desc()).offset(abs(position) - 1).limit(1)

        result = self.session.exec(statement).first()
        return Tag(**result.model_dump()) if result else None


    def select_tag_by_id(self, tag_id: int, with_rooms: bool = False) -> Tag:
        tag_model = self.session.get(TagModel, tag_id)
        if not tag_model:
            raise NotFoundError("Tag", tag_id)

        if with_rooms:
            return Tag(
                **tag_model.model_dump(),
                rooms=[
                    {
                        **room_tag.model_dump(),
                        "room": {
                            **room_tag.room.model_dump(),
                            "building": room_tag.room.building.model_dump()
                            if room_tag.room and room_tag.room.building else None,
                        },
                    }
                    for room_tag in tag_model.room_tags
                ],
            )
        else:
            return Tag(**tag_model.model_dump())

    def update_tag(self, tag_id: int, tag_data: dict) -> Tag:
        try:
            tag_model = self.session.get(TagModel, tag_id)
            if not tag_model:
                raise NotFoundError("Tag", tag_id)

            updated_fields = 0

            for key, value in tag_data.items():
                if not hasattr(tag_model, key):
                    continue 
                current_value = getattr(tag_model, key, None)  # optimise : win 0.00025s
                if current_value != value:
                    setattr(tag_model, key, value)
                    updated_fields = 1

            if updated_fields:
                self.session.flush()
                self.session.commit()
                self.session.refresh(tag_model)

            return Tag.from_dict(tag_model.model_dump())

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.UniqueViolation):
                raise AlreadyExistsError("Tag", "source_address", tag_data["source_address"]) from e
            elif isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Tag", constraint_name, table_name) from e
            logger.error(e)
            raise UpdateFailedError("Tag", "Integrity error") from e
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise UpdateFailedError("Tag", str(e)) from e


    def delete_tag(self, tag_id: int) -> bool:
        try:
            tag_model = self.session.get(TagModel, tag_id)

            if not tag_model:
                raise NotFoundError("Tag", tag_id)

            statement = select(RoomTagModel).where(RoomTagModel.tag_id == tag_id)
            room_tags = self.session.exec(statement).all()

            if room_tags:
                now = datetime.now()
                for rt in room_tags:
                    rt.end_at = now
                self.session.commit()
                return True
            else:
                self.session.delete(tag_model)
                self.session.commit()
                return True

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Tag", constraint_name, table_name) from e

            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise DeletionFailedError("Tag", str(e)) from e


    def select_tag_by_src_address(self, tag_src_address: str) -> Tag:
        statement = select(TagModel).where(TagModel.source_address == tag_src_address)
        tag_model = self.session.exec(statement).first()

        if not tag_model:
            raise NotFoundError("Tag", tag_src_address, "source_address")

        return Tag(**tag_model.model_dump())


    def create_with_room_link(self, tag: Tag, room_id: int, start_at: datetime, end_at: datetime | None = None) -> Tag:
        try:       
            tag_model = TagModel(
                name=tag.name,
                description=tag.description,
                source_address=tag.source_address,
            )
            self.session.add(tag_model)
            self.session.flush()

            new_tag = Tag.from_dict(tag_model.model_dump())

            room_tag_model = RoomTagModel(
                tag_id=tag_model.id,
                room_id=room_id,
                start_at=start_at,
                end_at=end_at
            )
            self.session.add(room_tag_model)
            self.session.flush()
            self.session.commit()

            new_tag.rooms = [
                {
                    **room_tag.model_dump(),
                    "room": {
                        **room_tag.room.model_dump(),
                        "building": room_tag.room.building.model_dump()
                        if room_tag.room and room_tag.room.building else None,
                    },
                }
                for room_tag in tag_model.room_tags
            ]
            return new_tag

        except IntegrityError as e:
            self.session.rollback()
            orig = getattr(e, "orig", None)
            if orig :
                if isinstance(e.orig, errors.UniqueViolation):
                    raise AlreadyExistsError("Tag", "source_address", tag_model.source_address) from e
                
                if isinstance(e.orig, errors.ForeignKeyViolation):
                    constraint_name = getattr(e.orig.diag, "constraint_name", None)
                    table_name = getattr(e.orig.diag, "table_name", None)
                    raise ForeignKeyConstraintError("RoomTag", constraint_name, table_name) from e
            
                if isinstance(e.orig, errors.CheckViolation):
                    constraint_name = getattr(e.orig.diag, "constraint_name", None)
                    table_name = getattr(e.orig.diag, "table_name", None)
                    raise CheckConstraintError("RoomTag", constraint_name, table_name) from e
                
            logger.error(e)
            raise CreationFailedError("Tag", "Integrity error") from e
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            orig = getattr(e, "orig", None)
            
            if orig and (isinstance(e.orig, errors.RaiseException) or "Already exist" in str(e.orig)):
                raise AlreadyExistsError("RoomTag", "room_id, tag_id", f"room_id={room_id} and tag_id={tag_model.id}") from e
            
            raise CreationFailedError("TagWithRoomlink", str(e)) from e