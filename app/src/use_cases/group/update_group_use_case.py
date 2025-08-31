from app.src.domain.entities.group import Group
from app.src.domain.interface_repositories.group_repository import GroupRepository


class UpdateGroupUseCase:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    def execute(self, group_id: int, group_data: dict) -> Group:
        return self.group_repository.update_group(group_id, group_data)

    def get(self, group_id: int) -> Group:
        group = self.group_repository.select_group_by_id(group_id)

        return group
