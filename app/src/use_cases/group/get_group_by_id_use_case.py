from app.src.domain.entities.group import Group
from app.src.domain.interface_repositories.group_repository import GroupRepository


class GetGroupByIdUseCase:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    def execute(self, group_id: int) -> Group:
        group = self.group_repository.select_group_by_id(group_id)

        return group
