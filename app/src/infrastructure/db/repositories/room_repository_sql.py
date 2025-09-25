import logging

from psycopg2 import errors
from sqlalchemy import func, text
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.room import Room
from app.src.infrastructure.db.models.room_model import RoomModel
from app.src.domain.interface_repositories.room_repository import RoomRepository
from app.src.common.exception import (
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)


logger = logging.getLogger(__name__)


class SQLRoomRepository(RoomRepository):
    def __init__(self, session: Session):
        self.session = session


    def create_room(self, room: Room) -> Room:
        try:
            room_model = RoomModel(
                name=room.name,
                description=room.description,
                floor=room.floor,
                building_id=room.building_id,
                area=room.area,
                shape=room.shape,
                capacity=room.capacity,
                start_at=room.start_at,
                end_at=room.end_at,
            )
            self.session.add(room_model)
            self.session.flush()
            self.session.commit()
            self.session.refresh(room_model)

        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Room", constraint_name, table_name) from e
            logger.error(e)
            raise UpdateFailedError("Room", "Integrity error") from e
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise CreationFailedError("Room", str(e)) from e

        return Room.from_dict(room_model.model_dump())
    

    def select_rooms(self, offset: int | None = None, limit: int | None = None) -> list[Room]:
        statement = select(RoomModel).order_by(RoomModel.created_at.desc())

        if offset is not None:
            statement = statement.offset(offset)

        if limit is not None:
            statement = statement.limit(limit)

        results = self.session.exec(statement).all()
        return [Room(**room.model_dump()) for room in results]
    

    def count_all_rooms(self) -> int:
        total = self.session.exec(select(func.count()).select_from(RoomModel)).one()
        return total


    def select_room_by_id(self, room_id: int) -> Room:
        room_model = self.session.get(RoomModel, room_id)
        if not room_model:
            raise NotFoundError("Room", room_id)

        return Room(**room_model.model_dump())


    def update_room(self, room_id: int, room_data: dict) -> Room:
        try:
            room_model = self.session.get(RoomModel, room_id)
            if not room_model:
                raise NotFoundError("Room", room_id)

            updated_fields = 0

            for key, value in room_data.items():
                if not hasattr(room_model, key):
                    continue 
                current_value = getattr(room_model, key, None) 
                if current_value != value:
                    setattr(room_model, key, value)
                    updated_fields = 1

            if updated_fields:
                self.session.flush()
                self.session.commit()
                self.session.refresh(room_model)

            return Room.from_dict(room_model.model_dump())

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            logger.error(e)
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Room", constraint_name, table_name) from e
            raise UpdateFailedError("Room", "Integrity error") from e
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise UpdateFailedError("Room", str(e)) from e
        

    def delete_room(self, room_id: int) -> bool:
        try:
            room_model = self.session.get(RoomModel, room_id)

            if not room_model:
                raise NotFoundError("Room", room_id)

            self.session.delete(room_model)
            self.session.commit()
            return True

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            logger.error(e)
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Room", constraint_name, table_name) from e

            raise DeletionFailedError("Room", "Integrity error") from e
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise DeletionFailedError("Room", str(e)) from e



    def paginate_rooms_with_tags(self, cursor: int | None, limit: InterruptedError) -> tuple[list[Room], int, Room | None, Room | None]:       
        tags = self.select_rooms_with_tags(cursor, limit)
        total = self.count_all_rooms()
        first_tag = self.get_room_by_position(0)
        last_page_offset = (
            (total // (limit - 1)) * (limit - 1)
            if total % (limit - 1) != 0
            else ((total // (limit - 1)) - 1) * (limit - 1)
        )

        last_tag = self.get_room_by_position(last_page_offset)

        return tags, total, first_tag, last_tag


    def select_rooms_with_tags(self, cursor: int | None, limit: int) -> list[Room]:
        statement = select(RoomModel).order_by(RoomModel.id)

        if cursor:
            statement = statement.where(RoomModel.id >= cursor)
        statement = statement.limit(limit)

        results = self.session.exec(statement).all()
  
        return [
            Room(
                **room.model_dump(),
                tags=[
                    {
                        **room_tag.model_dump(),
                        "tag": room_tag.tag.model_dump() if room_tag.tag else None
                    }
                    for room_tag in room.room_tags
                ],
            )
            for room in results
        ]




    def get_room_by_position(self, position: int) -> Room | None:
        if position >= 0:
            statement = select(RoomModel).order_by(RoomModel.id.asc()).offset(position).limit(1)
        else:
            statement = select(RoomModel).order_by(RoomModel.id.desc()).offset(abs(position) - 1).limit(1)

        result = self.session.exec(statement).first()
        return Room(**result.model_dump()) if result else None

