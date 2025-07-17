from app.src.common.exception import NotFoundError
from app.src.domain.entities.tag import Tag
from app.src.domain.interface_repositories.tag_repository import TagRepository


class GetTagByIdUseCase:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def execute(self, tag_id: int) -> Tag:
        tag = self.tag_repository.select_tag_by_id(tag_id)

        if not tag:
            raise NotFoundError("Tag", tag_id)

        return tag
