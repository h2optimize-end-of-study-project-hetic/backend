from app.src.infrastructure.db.repositories.view_repository_sql import GroupUserRepository
from app.src.common.exception import NotFoundError
from app.src.infrastructure.db.models.user_model import UserModel


class GetUsersInGroupUseCase:
    def __init__(self, repository: GroupUserRepository):
        self.repository = repository

    def execute(self, group_id: int) -> list[UserModel]:
        group = self.repository.get_group_by_id(group_id)
        if not group:
            raise NotFoundError("Group", group_id)

        return self.repository.get_users_in_group(group_id)
