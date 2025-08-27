import logging

from psycopg2 import errors
from sqlalchemy import func, text
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.event_room import EventRoom
from app.src.infrastructure.db.models.event_room_model import EventRoomModel
from app.src.domain.interface_repositories.event_room_repository import EventRoomRepository
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

logger = logging.getLogger(__name__)


class SQLEventRoomRepository(EventRoomRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_event_room(self, event_room: EventRoom) -> EventRoom:
        try:
            event_room_model = EventRoomModel(
                event_id=event_room.event_id,
                room_id=event_room.room_id,
                is_finished=event_room.is_finished,
                start_at=event_room.start_at,
                end_at=event_room.end_at,
            )
            self.session.add(event_room_model)
            self.session.flush()
            self.session.commit()
            self.session.refresh(event_room_model)
        except IntegrityError as e:
            self.session.rollback()
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise CreationFailedError("EventRoom", str(e)) from e

        return EventRoom.from_dict(event_room_model.model_dump())

    def paginate_event_rooms(self, cursor: int | None, limit: int) -> tuple[list[EventRoom], int, EventRoom | None, EventRoom | None]:
        self.session.exec(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"))

        event_rooms = self.select_event_rooms(cursor, limit)
        total = self.count_all_event_rooms()
        first_event_room = self.get_event_room_by_position(0)
        last_page_offset = (
            (total // (limit - 1)) * (limit - 1)
            if total % (limit - 1) != 0
            else ((total // (limit - 1)) - 1) * (limit - 1)
        )

        last_event_room = self.get_event_room_by_position(last_page_offset)

        return event_rooms, total, first_event_room, last_event_room

    def select_event_rooms(self, cursor: int | None, limit: int) -> list[EventRoom]:
        statement = select(EventRoomModel).order_by(EventRoomModel.id)
        if cursor:
            statement = statement.where(EventRoomModel.id >= cursor)
        statement = statement.limit(limit)

        results = self.session.exec(statement).all()
        return [EventRoom(**event_room.model_dump()) for event_room in results]

    def count_all_event_rooms(self) -> int:
        total = self.session.exec(select(func.count()).select_from(EventRoomModel)).one()
        return total

    def get_event_room_by_position(self, position: int) -> EventRoom | None:
        if position >= 0:
            statement = select(EventRoomModel).order_by(EventRoomModel.id.asc()).offset(position).limit(1)
        else:
            statement = select(EventRoomModel).order_by(EventRoomModel.id.desc()).offset(abs(position) - 1).limit(1)

        result = self.session.exec(statement).first()
        return EventRoom(**result.model_dump()) if result else None

    def select_event_room_by_id(self, event_room_id: int) -> EventRoom:
        event_room_model = self.session.get(EventRoomModel, event_room_id)
        if not event_room_model:
            raise NotFoundError("EventRoom", event_room_id)

        return EventRoom(**event_room_model.model_dump())

    def update_event_room(self, event_room_id: int, event_room_data: dict) -> EventRoom:
        try:
            event_room_model = self.session.get(EventRoomModel, event_room_id)
            if not event_room_model:
                raise NotFoundError("EventRoom", event_room_id)

            updated_fields = 0

            for key, value in event_room_data.items():
                current_value = getattr(event_room_model, key, None)  # optimise : win 0.00025s
                if current_value != value:
                    setattr(event_room_model, key, value)
                    updated_fields = 1

            if updated_fields:
                self.session.flush()
                self.session.commit()
                self.session.refresh(event_room_model)

            return EventRoom.from_dict(event_room_model.model_dump())

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.UniqueViolation):
                raise AlreadyExistsError("EventRoom", "source_address", event_room_data["source_address"]) from e
            elif isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("EventRoom", constraint_name, table_name) from e
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise UpdateFailedError("EventRoom", str(e)) from e

    def delete_event_room(self, event_room_id: int) -> bool:
        try:
            event_room_model = self.session.get(EventRoomModel, event_room_id)

            if not event_room_model:
                raise NotFoundError("EventRoom", event_room_id)

            self.session.delete(event_room_model)
            self.session.commit()
            return True

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("EventRoom", constraint_name, table_name) from e

            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise DeletionFailedError("EventRoom", str(e)) from e


    def get_event_room(self, event_room_id: int) -> EventRoom:
        return self.session.query(EventRoom).filter(EventRoom.id == event_room_id).first()