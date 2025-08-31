from app.src.domain.entities.user_group import UserGroup
from app.src.domain.interface_repositories.user_group_repository import UserGroupRepository


class GetUserGroupByIdUseCase:
    def __init__(self, user_group_repository: UserGroupRepository):
        self.user_group_repository = user_group_repository

    def execute(self, user_id: int, group_id: int) -> UserGroup:
        user_group = self.user_group_repository.select_user_group_by_id(user_id, group_id)
        return user_group