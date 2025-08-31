import logging

from psycopg2 import errors
from sqlalchemy import func, text
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.user_group import UserGroup
from app.src.infrastructure.db.models.user_group_model import UserGroupModel
from app.src.domain.interface_repositories.user_group_repository import UserGroupRepository
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

logger = logging.getLogger(__name__)


class SQLUserGroupRepository(UserGroupRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_user_group(self, user_group: UserGroup) -> UserGroup:
        try:
            user_group_model = UserGroupModel(
                group_id=user_group.group_id,
                user_id=user_group.user_id,
            )
            self.session.add(user_group_model)
            self.session.flush()
            self.session.commit()
            self.session.refresh(user_group_model)
        except IntegrityError as e:
            self.session.rollback()
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise CreationFailedError("UserGroup", str(e)) from e

        return UserGroup.from_dict(user_group_model.model_dump())

    def paginate_user_groups(self, cursor: tuple[int, int] | None, limit: int) -> tuple[list[UserGroup], int, UserGroup | None, UserGroup | None]:

        user_groups = self.select_user_groups(cursor, limit)
        total = self.count_all_user_groups()
        first_user_group = self.get_user_group_by_position(0)
        last_page_offset = (
            (total // (limit - 1)) * (limit - 1)
            if total % (limit - 1) != 0
            else ((total // (limit - 1)) - 1) * (limit - 1)
        )

        last_user_group = self.get_user_group_by_position(last_page_offset)

        return user_groups, total, first_user_group, last_user_group

    def select_user_groups(self, cursor: tuple[int,int] | None, limit: int) -> list[UserGroup]:
        statement = select(UserGroupModel).order_by(UserGroupModel.user_id, UserGroupModel.group_id)

        if cursor:
            statement = statement.where((UserGroupModel.user_id, UserGroupModel.group_id) >= cursor)
        statement = statement.limit(limit)

        results = self.session.exec(statement).all()
        return [UserGroup(**user_group.model_dump()) for user_group in results]

    def count_all_user_groups(self) -> int:
        total = self.session.exec(select(func.count()).select_from(UserGroupModel)).one()
        return total

    def get_user_group_by_position(self, position: int) -> UserGroup | None:
        statement = select(UserGroupModel).order_by(UserGroupModel.user_id, UserGroupModel.group_id)
        if position >= 0:
            statement = select(UserGroupModel).order_by(UserGroupModel.user_id.asc(), UserGroupModel.group_id.asc()).offset(position).limit(1)
        else:
            statement = select(UserGroupModel).order_by(UserGroupModel.user_id.desc(), UserGroupModel.group_id.desc()).offset(abs(position) - 1).limit(1)

        result = self.session.exec(statement).first()
        return UserGroup(**result.model_dump()) if result else None

    def select_user_group_by_id(self, user_id: int, group_id: int) -> UserGroup:
        statement = select(UserGroupModel).where(
            UserGroupModel.user_id == user_id,
            UserGroupModel.group_id == group_id
        )
        result = self.session.exec(statement).first()
        if not result:
            raise NotFoundError("UserGroup", f"user_id={user_id}, group_id={group_id}")

        return UserGroup(**result.model_dump())

    def update_user_group(self, user_id: int, group_id: int, user_group_data: dict) -> UserGroup:
        try:
            statement = select(UserGroupModel).where(
                UserGroupModel.user_id == user_id,
                UserGroupModel.group_id == group_id
            )
            user_group_model = self.session.exec(statement).first()
            if not user_group_model:
                raise NotFoundError("UserGroup", f"user_id={user_id}, group_id={group_id}")

            updated_fields = 0

            for key, value in user_group_data.items():
                current_value = getattr(user_group_model, key, None)  # optimise : win 0.00025s
                if current_value != value:
                    setattr(user_group_model, key, value)
                    updated_fields = 1

            if updated_fields:
                self.session.flush()
                self.session.commit()
                self.session.refresh(user_group_model)

            return UserGroup.from_dict(user_group_model.model_dump())

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            # if isinstance(e.orig, errors.UniqueViolation):
            #     raise AlreadyExistsError("UserGroup", "source_address", user_group_data["source_address"]) from e
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("UserGroup", constraint_name, table_name) from e
            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise UpdateFailedError("UserGroup", str(e)) from e

    def delete_user_group(self, user_id: int, group_id: int) -> bool:
        try:
            statement = select(UserGroupModel).where(
                UserGroupModel.user_id == user_id,
                UserGroupModel.group_id == group_id
            )
            user_group_model = self.session.exec(statement).first()

            if not user_group_model:
                raise NotFoundError("UserGroup", f"user_id={user_id}, group_id={group_id}")

            self.session.delete(user_group_model)
            self.session.commit()
            return True

        except NotFoundError:
            raise
        except IntegrityError as e:
            self.session.rollback()
            if isinstance(e.orig, errors.ForeignKeyViolation):
                constraint_name = getattr(e.orig.diag, "constraint_name", None)
                table_name = getattr(e.orig.diag, "table_name", None)
                raise ForeignKeyConstraintError("UserGroup", constraint_name, table_name) from e

            logger.error(e)
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise DeletionFailedError("UserGroup", str(e)) from e


    def get_user_group(self, user_group_id: int) -> UserGroup:
        return self.session.query(UserGroup).filter(UserGroup.id == user_group_id).first()