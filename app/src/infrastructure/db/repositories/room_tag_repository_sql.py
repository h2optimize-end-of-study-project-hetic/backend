from datetime import datetime
import logging

from psycopg2 import errors
from sqlalchemy import func, or_, and_
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.room_tag import RoomTag
from app.src.domain.interface_repositories.room_tag_repository import RoomTagRepository
from app.src.infrastructure.db.models.room_tag_model import RoomTagModel
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


class SQLRoomTagRepository(RoomTagRepository):
    def __init__(self, session: Session):
        self.session = session


    def create_roomtag(self, room_tag: RoomTag) -> RoomTag:
        try:
            room_tag_model = RoomTagModel(
                tag_id=room_tag.tag_id,
                room_id=room_tag.room_id,
                start_at=room_tag.start_at,
                end_at=room_tag.end_at
            )
            self.session.add(room_tag_model)
            self.session.flush()
            self.session.commit()
            self.session.refresh(room_tag_model)

            return RoomTag.from_dict(room_tag_model.model_dump())
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("RoomTag", constraint_name, table_name) from e
        
            if isinstance(e.orig, errors.CheckViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise CheckConstraintError("RoomTag", constraint_name, table_name) from e

            logger.error(e)
            raise CreationFailedError("RoomTag", "Integrity error") from e
        except Exception as e:
            self.session.rollback()
            logger.error(e)

            if isinstance(e.orig, errors.RaiseException) or "Already exist" in str(e.orig):
                raise AlreadyExistsError("RoomTag", "room_id, tag_id", f"room_id={room_tag.room_id} and tag_id={room_tag.tag_id}") from e
            
            raise CreationFailedError("RoomTag", str(e)) from e
    


    def paginate_roomtag(self, cursor: int | None, limit: int, active_only: bool = False) -> tuple[list[RoomTag], int, RoomTag | None, RoomTag | None]:
        room_tags = self.select_roomtag(cursor, limit, active_only)
        total = self.count_all_roomtag(active_only)
        first_room_tag = self.get_roomtag_by_position(0, active_only)
        last_page_offset = (
            (total // (limit - 1)) * (limit - 1)
            if total % (limit - 1) != 0
            else ((total // (limit - 1)) - 1) * (limit - 1)
        )
        last_room_tag = self.get_roomtag_by_position(last_page_offset, active_only)

        return room_tags, total, first_room_tag, last_room_tag


    def select_roomtag(self, cursor: int | None, limit: int, active_only: bool = False) -> list[RoomTag]:
        statement = select(RoomTagModel).order_by(RoomTagModel.id)
        if cursor:
            statement = statement.where(RoomTagModel.id >= cursor)

        if active_only:
            now = datetime.now()
            statement = statement.where(
                and_(
                    or_(RoomTagModel.start_at is None, RoomTagModel.start_at <= now),
                    or_(RoomTagModel.end_at is None, RoomTagModel.end_at >= now)
                )
            )

        statement = statement.limit(limit)
        results = self.session.exec(statement).all()
        return [RoomTag(**room_tag.model_dump()) for room_tag in results]


    def count_all_roomtag(self, active_only: bool = False) -> int:
        statement = select(func.count()).select_from(RoomTagModel)
        if active_only:
            now = datetime.now()
            statement = statement.where(
                and_(
                    or_(RoomTagModel.start_at is None, RoomTagModel.start_at <= now),
                    or_(RoomTagModel.end_at is None, RoomTagModel.end_at >= now)
                )
            )
        return self.session.exec(statement).one()


    def get_roomtag_by_position(self, position: int, active_only: bool = False) -> RoomTag | None:
        if position >= 0:
            statement = select(RoomTagModel).order_by(RoomTagModel.id.asc()).offset(position).limit(1)
        else:
            statement = select(RoomTagModel).order_by(RoomTagModel.id.desc()).offset(abs(position) - 1).limit(1)

        if active_only:
            now = datetime.now()
            statement = statement.where(
                and_(
                    or_(RoomTagModel.start_at is None, RoomTagModel.start_at <= now),
                    or_(RoomTagModel.end_at is None, RoomTagModel.end_at >= now)
                )
            )

        result = self.session.exec(statement).first()
        return RoomTag(**result.model_dump()) if result else None


    def select_roomtag_by_id(self, tag_id: int) -> RoomTag:
        tag_model = self.session.get(RoomTagModel, tag_id)
        if not tag_model:
            raise NotFoundError("RoomTag", tag_id)

        return RoomTag(**tag_model.model_dump())


    def update_roomtag(self, room_tag_id: int, tag_data: dict) -> RoomTag:
        try:
            room_tag_model = self.session.get(RoomTagModel, room_tag_id)
            if not room_tag_model:
                raise NotFoundError("RoomTag", room_tag_id)

            updated_fields = 0

            for key, value in tag_data.items():
                if not hasattr(room_tag_model, key):
                    continue 
                current_value = getattr(room_tag_model, key, None)  # optimise : win 0.00025s
                if current_value != value:
                    setattr(room_tag_model, key, value)
                    updated_fields = 1

            if updated_fields:
                self.session.flush()
                self.session.commit()
                self.session.refresh(room_tag_model)

            return RoomTag.from_dict(room_tag_model.model_dump())
        
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("RoomTag", constraint_name, table_name) from e
        
            if isinstance(e.orig, errors.CheckViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise CheckConstraintError("RoomTag", constraint_name, table_name) from e

            logger.error(e)
            raise UpdateFailedError("RoomTag", "Integrity error") from e
        
        except Exception as e:
            self.session.rollback()
            logger.error(e)

            if isinstance(e.orig, errors.RaiseException) or "Already exist" in str(e.orig):
                raise AlreadyExistsError("RoomTag", "room_id, tag_id", f"room_id={room_tag_id} and tag_id={room_tag_id}") from e
            
            raise CreationFailedError("RoomTag", str(e)) from e


    def delete_roomtag(self, room_tag_id: int) -> bool:
        try:
            tag_model = self.session.get(RoomTagModel, room_tag_id)

            if not tag_model:
                raise NotFoundError("RoomTag", room_tag_id)

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
                raise ForeignKeyConstraintError("RoomTag", constraint_name, table_name) from e

            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise DeletionFailedError("RoomTag", str(e)) from e
    

    def update_roomtag_by_tag_id_room_id(self, tag_id: int, room_id: int, start_at: datetime, end_at: datetime | None) -> RoomTag:
        try:
            statement = select(RoomTagModel).where(
                and_(
                    RoomTagModel.tag_id == tag_id,
                    RoomTagModel.room_id == room_id,
                )
            )
            room_tag_model = self.session.exec(statement).first()

            if room_tag_model:
                room_tag_model.start_at = start_at
                room_tag_model.end_at = end_at
            else:
                room_tag_model = RoomTagModel(
                    tag_id=tag_id,
                    room_id=room_id,
                    start_at=start_at,
                    end_at=end_at,
                )
                self.session.add(room_tag_model)

            self.session.commit()
            self.session.refresh(room_tag_model)
            return RoomTag.from_dict(room_tag_model.model_dump())

        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("RoomTag", constraint_name, table_name) from e

            if isinstance(e.orig, errors.CheckViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise CheckConstraintError("RoomTag", constraint_name, table_name) from e

            logger.error(e)
            raise UpdateFailedError("RoomTag", "Integrity error") from e
        except Exception as e:
            self.session.rollback()
            logger.error(e)

            if isinstance(e.orig, errors.RaiseException) or "Already exist" in str(e.orig):
                raise AlreadyExistsError("RoomTag", "room_id, tag_id", f"room_id={room_id} and tag_id={tag_id}") from e
            
            raise UpdateFailedError("RoomTag", str(e)) from e