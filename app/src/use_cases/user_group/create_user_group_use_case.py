from app.src.domain.entities.user_group import UserGroup
from app.src.domain.interface_repositories.user_group_repository import UserGroupRepository


class CreateUserGroupUseCase:
    def __init__(self, user_group_repository: UserGroupRepository):
        self.user_group_repository = user_group_repository

    def execute(self, user_group: UserGroup) -> UserGroup:
        return self.user_group_repository.create_user_group(user_group)
