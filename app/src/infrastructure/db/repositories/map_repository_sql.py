import logging

from psycopg2 import errors
from sqlalchemy import func, text
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.map import Map
from app.src.infrastructure.db.models.map_model import MapModel
from app.src.domain.interface_repositories.map_repository import MapRepository
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

logger = logging.getLogger(__name__)


class SQLMapRepository(MapRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_map(self, map: Map) -> Map:
        try:
            map_model = MapModel(
                building_id=map.building_id,
                file_name=map.file_name,
                floor=map.floor,
                path=map.path,
                width=map.width,
                length=map.length,
            )
            self.session.add(map_model)
            self.session.flush()
            self.session.commit()
            self.session.refresh(map_model)
        except IntegrityError as e:
            self.session.rollback()
        #     if isinstance(e.orig, errors.UniqueViolation):
        #         raise AlreadyExistsError("Map", "source_address", map_model.source_address) from e
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise CreationFailedError("Map", str(e)) from e

        return Map.from_dict(map_model.model_dump())

    def paginate_maps(self, cursor: int | None, limit: int) -> tuple[list[Map], int, Map | None, Map | None]:

        maps = self.select_maps(cursor, limit)
        total = self.count_all_maps()
        first_map = self.get_map_by_position(0)
        last_page_offset = (
            (total // (limit - 1)) * (limit - 1)
            if total % (limit - 1) != 0
            else ((total // (limit - 1)) - 1) * (limit - 1)
        )

        last_map = self.get_map_by_position(last_page_offset)

        return maps, total, first_map, last_map

    def select_maps(self, cursor: int | None, limit: int) -> list[Map]:
        statement = select(MapModel).order_by(MapModel.id)
        if cursor:
            statement = statement.where(MapModel.id >= cursor)
        statement = statement.limit(limit)

        results = self.session.exec(statement).all()
        return [Map(**map.model_dump()) for map in results]

    def count_all_maps(self) -> int:
        total = self.session.exec(select(func.count()).select_from(MapModel)).one()
        return total

    def get_map_by_position(self, position: int) -> Map | None:
        if position >= 0:
            statement = select(MapModel).order_by(MapModel.id.asc()).offset(position).limit(1)
        else:
            statement = select(MapModel).order_by(MapModel.id.desc()).offset(abs(position) - 1).limit(1)

        result = self.session.exec(statement).first()
        return Map(**result.model_dump()) if result else None

    def select_map_by_id(self, map_id: int) -> Map:
        map_model = self.session.get(MapModel, map_id)
        if not map_model:
            raise NotFoundError("Map", map_id)

        return Map(**map_model.model_dump())

    def update_map(self, map_id: int, map_data: dict) -> Map:
        try:
            map_model = self.session.get(MapModel, map_id)
            if not map_model:
                raise NotFoundError("Map", map_id)

            updated_fields = 0

            for key, value in map_data.items():
                current_value = getattr(map_model, key, None)  # optimise : win 0.00025s
                if current_value != value:
                    setattr(map_model, key, value)
                    updated_fields = 1

            if updated_fields:
                self.session.flush()
                self.session.commit()
                self.session.refresh(map_model)

            return Map.from_dict(map_model.model_dump())

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.UniqueViolation):
                raise AlreadyExistsError("Map", "source_address", map_data["source_address"]) from e
            elif isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Map", constraint_name, table_name) from e
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise UpdateFailedError("Map", str(e)) from e

    def delete_map(self, map_id: int) -> bool:
        try:
            map_model = self.session.get(MapModel, map_id)

            if not map_model:
                raise NotFoundError("Map", map_id)

            self.session.delete(map_model)
            self.session.commit()
            return True

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Map", constraint_name, table_name) from e

            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise DeletionFailedError("Map", str(e)) from e


    def get_map(self, map_id: int) -> Map:
        return self.session.query(Map).filter(Map.id == map_id).first()
