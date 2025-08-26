import datetime
from sqlmodel import Session, select
from sqlalchemy import func
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from app.src.common.exception import NotFoundError, UpdateFailedError


from app.src.domain.entities.user import User
from app.src.infrastructure.db.models.user_model import UserModel
from app.src.domain.interface_repositories.user_repository import UserRepository

class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        user_model = UserModel(
            email=user.email,
            password=user.password,
            salt=user.salt,
            secret_2fa=user.secret_2fa,
            firstname=user.firstname,
            lastname=user.lastname,
            role=user.role.value if hasattr(user.role, "value") else user.role,
            phone_number=user.phone_number,
            is_active=user.is_active,
            is_delete=user.is_delete,
            created_at=user.created_at,
            updated_at=user.updated_at,
            deleted_at=user.deleted_at,
        )
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        return User(
            id=user_model.id,
            email=user_model.email,
            password=user_model.password,
            salt=user_model.salt,
            secret_2fa=user_model.secret_2fa,
            firstname=user_model.firstname,
            lastname=user_model.lastname,
            role=user_model.role,
            phone_number=user_model.phone_number,
            is_active=user_model.is_active,
            is_delete=user_model.is_delete,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            deleted_at=user_model.deleted_at,
        )

    def select_users(self, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Optional[User]]:
        statement = select(UserModel)
        if offset is not None:
            statement = statement.offset(offset)
        if limit is not None:
            statement = statement.limit(limit)
        results = self.session.exec(statement).all()
        return [
            User(
                id=user.id,
                email=user.email,
                password=user.password,
                salt=user.salt,
                secret_2fa=user.secret_2fa,
                firstname=user.firstname,
                lastname=user.lastname,
                role=user.role,
                phone_number=user.phone_number,
                is_active=user.is_active,
                is_delete=user.is_delete,
                created_at=user.created_at,
                updated_at=user.updated_at,
                deleted_at=user.deleted_at,
            )
            for user in results
        ]

    def select_user_by_id(self, user_id: int) -> User:
        statement = select(UserModel).where(UserModel.id == user_id)
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError(f"User with ID {user_id} not found")
        return User(
            id=result.id,
            email=result.email,
            password=result.password,
            salt=result.salt,
            secret_2fa=result.secret_2fa,
            firstname=result.firstname,
            lastname=result.lastname,
            role=result.role,
            phone_number=result.phone_number,
            is_active=result.is_active,
            is_delete=result.is_delete,
            created_at=result.created_at,
            updated_at=result.updated_at,
            deleted_at=result.deleted_at,
        )

    def select_user_by_src_address(self, user_src_address: str) -> User:
        statement = select(UserModel).where(UserModel.email == user_src_address)
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError(f"User with email {user_src_address} not found")
        return User(
            id=result.id,
            email=result.email,
            password=result.password,
            salt=result.salt,
            secret_2fa=result.secret_2fa,
            firstname=result.firstname,
            lastname=result.lastname,
            role=result.role,
            phone_number=result.phone_number,
            is_active=result.is_active,
            is_delete=result.is_delete,
            created_at=result.created_at,
            updated_at=result.updated_at,
            deleted_at=result.deleted_at,
        )

    def update_user(self, user_id: int, user_data: dict) -> User:
        statement = select(UserModel).where(UserModel.id == user_id)
        user_model = self.session.exec(statement).first()
        if not user_model:
            raise ValueError(f"User with ID {user_id} not found")
        for key, value in user_data.items():
            if hasattr(user_model, key):
                setattr(user_model, key, value)
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        return User(
            id=user_model.id,
            email=user_model.email,
            password=user_model.password,
            salt=user_model.salt,
            secret_2fa=user_model.secret_2fa,
            firstname=user_model.firstname,
            lastname=user_model.lastname,
            role=user_model.role,
            phone_number=user_model.phone_number,
            is_active=user_model.is_active,
            is_delete=user_model.is_delete,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            deleted_at=user_model.deleted_at,
        )

    def delete_user(self, user_id: int) -> User:
        statement = select(UserModel).where(UserModel.id == user_id)
        user_model = self.session.exec(statement).first()
        if not user_model:
            raise ValueError(f"User with ID {user_id} not found")

        # Anonymisation des champs
        user_model.email = f"anonymized_{user_id}@example.com"
        user_model.firstname = "Anonymized"
        user_model.lastname = "User"
        user_model.password = ""
        user_model.salt = ""
        user_model.secret_2fa = None
        user_model.phone_number = None
        user_model.is_active = False
        user_model.is_delete = True
        user_model.updated_at = datetime.datetime.utcnow()

        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        return User(
            id=user_model.id,
            email=user_model.email,
            password=user_model.password,
            salt=user_model.salt,
            secret_2fa=user_model.secret_2fa,
            firstname=user_model.firstname,
            lastname=user_model.lastname,
            role=user_model.role,
            phone_number=user_model.phone_number,
            is_active=user_model.is_active,
            is_delete=user_model.is_delete,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            deleted_at=user_model.deleted_at,
        )        
    
    def paginate_users(self, cursor: Optional[int], limit: int):
        statement = select(UserModel)
        if cursor is not None:
            statement = statement.where(UserModel.id >= cursor)
        statement = statement.order_by(UserModel.id).limit(limit)
        results = self.session.exec(statement).all()
        total = self.session.exec(select(func.count()).select_from(UserModel)).one()
        total = total[0] if isinstance(total, tuple) else total
        first_user = results[0] if results else None
        last_user = results[-1] if results else None
        users = [
            User(
                id=user.id,
                email=user.email,
                password=user.password,
                salt=user.salt,
                secret_2fa=user.secret_2fa,
                firstname=user.firstname,
                lastname=user.lastname,
                role=user.role,
                phone_number=user.phone_number,
                is_active=user.is_active,
                is_delete=user.is_delete,
                created_at=user.created_at,
                updated_at=user.updated_at,
                deleted_at=user.deleted_at,
            )
            for user in results
        ]
        return users, total, first_user, last_user