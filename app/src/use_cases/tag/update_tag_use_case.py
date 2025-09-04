from app.src.domain.entities.tag import Tag
from app.src.domain.interface_repositories.tag_repository import TagRepository


class UpdateTagUseCase:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def execute(self, tag_id: int, tag_data: dict) -> Tag:
        return self.tag_repository.update_tag(tag_id, tag_data)
