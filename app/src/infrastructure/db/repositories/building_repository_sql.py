import logging

from psycopg2 import errors
from sqlalchemy import func, text
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.building import Building
from app.src.infrastructure.db.models.building_model import BuildingModel
from app.src.domain.interface_repositories.building_repository import BuildingRepository
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

logger = logging.getLogger(__name__)


class SQLBuildingRepository(BuildingRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_building(self, building: Building) -> Building:
        try:
            building_model = BuildingModel(
                name=building.name,
                description=building.description,
                room_count=building.room_count,
                street_number=building.street_number,
                street_name=building.street_name,
                postal_code=building.postal_code,
                city=building.city,
                country=building.country,
                latitude=building.latitude,
                longitude=building.longitude,
            )
            self.session.add(building_model)
            self.session.flush()
            self.session.commit()
            self.session.refresh(building_model)
        except IntegrityError as e:
            self.session.rollback()
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise CreationFailedError("Building", str(e)) from e

        return Building.from_dict(building_model.model_dump())

    def paginate_buildings(self, cursor: int | None, limit: int) -> tuple[list[Building], int, Building | None, Building | None]:

        buildings = self.select_buildings(cursor, limit)
        total = self.count_all_buildings()
        first_building = self.get_building_by_position(0)
        last_page_offset = (
            (total // (limit - 1)) * (limit - 1)
            if total % (limit - 1) != 0
            else ((total // (limit - 1)) - 1) * (limit - 1)
        )

        last_building = self.get_building_by_position(last_page_offset)

        return buildings, total, first_building, last_building

    def select_buildings(self, cursor: int | None, limit: int) -> list[Building]:
        statement = select(BuildingModel).order_by(BuildingModel.id)
        if cursor:
            statement = statement.where(BuildingModel.id >= cursor)
        statement = statement.limit(limit)

        results = self.session.exec(statement).all()
        return [Building(**building.model_dump()) for building in results]

    def count_all_buildings(self) -> int:
        total = self.session.exec(select(func.count()).select_from(BuildingModel)).one()
        return total

    def get_building_by_position(self, position: int) -> Building | None:
        if position >= 0:
            statement = select(BuildingModel).order_by(BuildingModel.id.asc()).offset(position).limit(1)
        else:
            statement = select(BuildingModel).order_by(BuildingModel.id.desc()).offset(abs(position) - 1).limit(1)

        result = self.session.exec(statement).first()
        return Building(**result.model_dump()) if result else None

    def select_building_by_id(self, building_id: int) -> Building:
        building_model = self.session.get(BuildingModel, building_id)
        if not building_model:
            raise NotFoundError("Building", building_id)

        return Building(**building_model.model_dump())

    def update_building(self, building_id: int, building_data: dict) -> Building:
        try:
            building_model = self.session.get(BuildingModel, building_id)
            if not building_model:
                raise NotFoundError("Building", building_id)

            updated_fields = 0

            for key, value in building_data.items():
                current_value = getattr(building_model, key, None)  # optimise : win 0.00025s
                if current_value != value:
                    setattr(building_model, key, value)
                    updated_fields = 1

            if updated_fields:
                self.session.flush()
                self.session.commit()
                self.session.refresh(building_model)

            return Building.from_dict(building_model.model_dump())

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.UniqueViolation):
                raise AlreadyExistsError("Building", "source_address", building_data["source_address"]) from e
            elif isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Building", constraint_name, table_name) from e
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise UpdateFailedError("Building", str(e)) from e

    def delete_building(self, building_id: int) -> bool:
        try:
            building_model = self.session.get(BuildingModel, building_id)

            if not building_model:
                raise NotFoundError("Building", building_id)

            self.session.delete(building_model)
            self.session.commit()
            return True

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Building", constraint_name, table_name) from e

            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise DeletionFailedError("Building", str(e)) from e


    def get_building(self, building_id: int) -> Building:
        return self.session.query(Building).filter(Building.id == building_id).first()