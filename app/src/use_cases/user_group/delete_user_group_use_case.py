from app.src.domain.interface_repositories.user_group_repository import UserGroupRepository


class DeleteUserGroupUseCase:
    def __init__(self, user_group_repository: UserGroupRepository):
        self.user_group_repository = user_group_repository

    def execute(self, user_id: int, group_id: int) -> bool:
        return self.user_group_repository.delete_user_group(user_id, group_id)
