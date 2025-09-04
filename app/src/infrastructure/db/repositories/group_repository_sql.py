import logging

from psycopg2 import errors
from sqlalchemy import func, text
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.group import Group
from app.src.infrastructure.db.models.group_model import GroupModel
from app.src.domain.interface_repositories.group_repository import GroupRepository
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

logger = logging.getLogger(__name__)


class SQLGroupRepository(GroupRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_group(self, group: Group) -> Group:
        try:
            group_model = GroupModel(
                
                name=group.name,
                description=group.description,
                member_count=group.member_count,
                start_at=group.start_at,
                end_at=group.end_at,
            )
            self.session.add(group_model)
            self.session.flush()
            self.session.commit()
            self.session.refresh(group_model)
        except IntegrityError as e:
            self.session.rollback()
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise CreationFailedError("Group", str(e)) from e

        return Group.from_dict(group_model.model_dump())

    def paginate_groups(self, cursor: int | None, limit: int) -> tuple[list[Group], int, Group | None, Group | None]:

        groups = self.select_groups(cursor, limit)
        total = self.count_all_groups()
        first_group = self.get_group_by_position(0)
        last_page_offset = (
            (total // (limit - 1)) * (limit - 1)
            if total % (limit - 1) != 0
            else ((total // (limit - 1)) - 1) * (limit - 1)
        )

        last_group = self.get_group_by_position(last_page_offset)

        return groups, total, first_group, last_group

    def select_groups(self, cursor: int | None, limit: int) -> list[Group]:
        statement = select(GroupModel).order_by(GroupModel.id)
        if cursor:
            statement = statement.where(GroupModel.id >= cursor)
        statement = statement.limit(limit)

        results = self.session.exec(statement).all()
        return [Group(**group.model_dump()) for group in results]

    def count_all_groups(self) -> int:
        total = self.session.exec(select(func.count()).select_from(GroupModel)).one()
        return total

    def get_group_by_position(self, position: int) -> Group | None:
        if position >= 0:
            statement = select(GroupModel).order_by(GroupModel.id.asc()).offset(position).limit(1)
        else:
            statement = select(GroupModel).order_by(GroupModel.id.desc()).offset(abs(position) - 1).limit(1)

        result = self.session.exec(statement).first()
        return Group(**result.model_dump()) if result else None

    def select_group_by_id(self, group_id: int) -> Group:
        group_model = self.session.get(GroupModel, group_id)
        if not group_model:
            raise NotFoundError("Group", group_id)

        return Group(**group_model.model_dump())

    def update_group(self, group_id: int, group_data: dict) -> Group:
        try:
            group_model = self.session.get(GroupModel, group_id)
            if not group_model:
                raise NotFoundError("Group", group_id)

            updated_fields = 0

            for key, value in group_data.items():
                current_value = getattr(group_model, key, None)  # optimise : win 0.00025s
                if current_value != value:
                    setattr(group_model, key, value)
                    updated_fields = 1

            if updated_fields:
                self.session.flush()
                self.session.commit()
                self.session.refresh(group_model)

            return Group.from_dict(group_model.model_dump())

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.UniqueViolation):
                raise AlreadyExistsError("Group", "source_address", group_data["source_address"]) from e
            elif isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Group", constraint_name, table_name) from e
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise UpdateFailedError("Group", str(e)) from e

    def delete_group(self, group_id: int) -> bool:
        try:
            group_model = self.session.get(GroupModel, group_id)

            if not group_model:
                raise NotFoundError("Group", group_id)

            self.session.delete(group_model)
            self.session.commit()
            return True

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("Group", constraint_name, table_name) from e

            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise DeletionFailedError("Group", str(e)) from e


    def get_group(self, group_id: int) -> Group:
        return self.session.query(Group).filter(Group.id == group_id).first()