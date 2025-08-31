from sqlmodel import select, Session
from app.src.infrastructure.db.models.user_model import UserModel
from app.src.infrastructure.db.models.user_group_model import UserGroupModel
from app.src.infrastructure.db.models.group_model import GroupModel

class GroupUserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_group_by_id(self, group_id: int) -> GroupModel | None:
        return self.session.get(GroupModel, group_id)

    def get_users_in_group(self, group_id: int) -> list[UserModel]:
        """
        Retourne tous les utilisateurs appartenant à un groupe donné.
        """
        statement = (
            select(UserModel)
            .join(UserGroupModel, UserGroupModel.user_id == UserModel.id)
            .join(GroupModel, UserGroupModel.group_id == GroupModel.id)
            .where(GroupModel.id == group_id)
            .order_by(UserModel.firstname)
        )

        results = self.session.exec(statement).all()
        return results
