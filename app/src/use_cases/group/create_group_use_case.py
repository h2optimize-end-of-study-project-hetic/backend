from app.src.domain.entities.group import Group
from app.src.domain.interface_repositories.group_repository import GroupRepository


class CreateGroupUseCase:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    def execute(self, group: Group) -> Group:
        return self.group_repository.create_group(group)
