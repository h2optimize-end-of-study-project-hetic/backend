from app.src.domain.interface_repositories.group_repository import GroupRepository


class DeleteGroupUseCase:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    def execute(self, group_id: int) -> bool:
        return self.group_repository.delete_group(group_id)
