import logging

from psycopg2 import errors
from sqlalchemy import func, text
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.tag import Tag
from app.src.infrastructure.db.models.tag_model import TagModel
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.domain.interface_repositories.room_repository import RoomRepository
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

logger = logging.getLogger(__name__)


class SQLTagRepository(TagRepository):
    def __init__(self, session: Session, room_repository: RoomRepository):
        self.session = session
        self.room_repository = room_repository

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
            raise
        except Exception as e:
            self.session.rollback()
            logging.error(e)
            raise CreationFailedError("Tag", str(e)) from e

        return Tag.from_dict(tag_model.model_dump())

    def create_tag_with_room(self, tag: Tag, room_id: int | None) -> Tag:
        try:
            # if room_id:
            # room = self.room_repository.select_room_by_id(room_id)
            # if not room:
            #     raise NotFoundError("Room", room_id)

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
            raise
        except Exception as e:
            self.session.rollback()
            logging.error(e)
            raise CreationFailedError("Tag", str(e)) from e

        return Tag.from_dict(tag_model.model_dump())

    def paginate_tags(self, cursor: int | None, limit: int) -> tuple[list[Tag], int, Tag | None, Tag | None]:
        self.session.exec(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"))

        tags = self.select_tags(cursor, limit)
        total = self.count_all_tags()
        first_tag = self.get_tag_by_position(0)
        last_tag = self.get_tag_by_position(max((-1 * limit), (-1 * total)))

        return tags, total, first_tag, last_tag

    def select_tags(self, cursor: int | None, limit: int) -> list[Tag]:
        statement = select(TagModel).order_by(TagModel.id)
        if cursor:
            statement = statement.where(TagModel.id >= cursor)
        statement = statement.limit(limit)

        results = self.session.exec(statement).all()
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

    def select_tag_by_id(self, tag_id: int) -> Tag | None:
        statement = select(TagModel).where(TagModel.id == tag_id)
        result = self.session.exec(statement).first()

        if not result:
            return None

        return Tag(**result.model_dump())

    def update_tag(self, tag_id: int, tag_data: dict) -> Tag:
        try:
            tag_model = self.session.get(TagModel, tag_id)
            if not tag_model:
                raise NotFoundError("Tag", tag_id)

            updated_fields = 0

            for key, value in tag_data.items():
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
                raise AlreadyExistsError("Tag", "source_address", tag_model.source_address) from e
            elif isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Tag", constraint_name, table_name) from e
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logging.error(e)
            raise UpdateFailedError("Tag", str(e)) from e

    def delete_tag(self, tag_id: int) -> bool:
        try:
            tag_model = self.session.get(TagModel, tag_id)

            if not tag_model:
                raise NotFoundError("Tag", tag_id)

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
        result = self.session.exec(statement).first()

        if not result:
            return None

        return Tag(**result.model_dump())
