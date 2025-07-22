from app.src.domain.entities.tag import Tag
from app.src.domain.interface_repositories.tag_repository import TagRepository


class CreateTagUseCase:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def execute(self, tag: Tag) -> Tag:
        return self.tag_repository.create_tag(tag)
