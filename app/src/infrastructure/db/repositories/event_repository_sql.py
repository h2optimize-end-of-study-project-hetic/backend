import logging

from psycopg2 import errors
from sqlalchemy import func, text
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.event import Event
from app.src.infrastructure.db.models.event_model import EventModel
from app.src.domain.interface_repositories.event_repository import EventRepository
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

logger = logging.getLogger(__name__)


class SQLEventRepository(EventRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_event(self, event: Event) -> Event:
        try:
            event_model = EventModel(
                name=event.name,
                description=event.description,
                group_id=event.group_id,
                supervisor=event.supervisor,
            )
            self.session.add(event_model)
            self.session.flush()
            self.session.commit()
            self.session.refresh(event_model)
        except IntegrityError as e:
            self.session.rollback()
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise CreationFailedError("Event", str(e)) from e

        return Event.from_dict(event_model.model_dump())

    def paginate_events(self, cursor: int | None, limit: int) -> tuple[list[Event], int, Event | None, Event | None]:
        self.session.exec(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"))

        events = self.select_events(cursor, limit)
        total = self.count_all_events()
        first_event = self.get_event_by_position(0)
        last_page_offset = (
            (total // (limit - 1)) * (limit - 1)
            if total % (limit - 1) != 0
            else ((total // (limit - 1)) - 1) * (limit - 1)
        )

        last_event = self.get_event_by_position(last_page_offset)

        return events, total, first_event, last_event

    def select_events(self, cursor: int | None, limit: int) -> list[Event]:
        statement = select(EventModel).order_by(EventModel.id)
        if cursor:
            statement = statement.where(EventModel.id >= cursor)
        statement = statement.limit(limit)

        results = self.session.exec(statement).all()
        return [Event(**event.model_dump()) for event in results]

    def count_all_events(self) -> int:
        total = self.session.exec(select(func.count()).select_from(EventModel)).one()
        return total

    def get_event_by_position(self, position: int) -> Event | None:
        if position >= 0:
            statement = select(EventModel).order_by(EventModel.id.asc()).offset(position).limit(1)
        else:
            statement = select(EventModel).order_by(EventModel.id.desc()).offset(abs(position) - 1).limit(1)

        result = self.session.exec(statement).first()
        return Event(**result.model_dump()) if result else None

    def select_event_by_id(self, event_id: int) -> Event:
        event_model = self.session.get(EventModel, event_id)
        if not event_model:
            raise NotFoundError("Event", event_id)

        return Event(**event_model.model_dump())

    def update_event(self, event_id: int, event_data: dict) -> Event:
        try:
            event_model = self.session.get(EventModel, event_id)
            if not event_model:
                raise NotFoundError("Event", event_id)

            updated_fields = 0

            for key, value in event_data.items():
                current_value = getattr(event_model, key, None)  # optimise : win 0.00025s
                if current_value != value:
                    setattr(event_model, key, value)
                    updated_fields = 1

            if updated_fields:
                self.session.flush()
                self.session.commit()
                self.session.refresh(event_model)

            return Event.from_dict(event_model.model_dump())

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.UniqueViolation):
                raise AlreadyExistsError("Event", "source_address", event_data["source_address"]) from e
            elif isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Event", constraint_name, table_name) from e
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise UpdateFailedError("Event", str(e)) from e

    def delete_event(self, event_id: int) -> bool:
        try:
            event_model = self.session.get(EventModel, event_id)

            if not event_model:
                raise NotFoundError("Event", event_id)

            self.session.delete(event_model)
            self.session.commit()
            return True

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Event", constraint_name, table_name) from e

            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise DeletionFailedError("Event", str(e)) from e


    def get_event(self, event_id: int) -> Event:
        return self.session.query(Event).filter(Event.id == event_id).first()
