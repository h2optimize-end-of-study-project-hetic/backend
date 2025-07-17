from app.src.domain.interface_repositories.tag_repository import TagRepository


class DeleteTagUseCase:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def execute(self, tag_id: int) -> bool:
        return self.tag_repository.delete_tag(tag_id)
