from app.src.domain.entities.tag import Tag
from app.src.domain.interface_repositories.tag_repository import TagRepository


class GetTagByIdUseCase:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def execute(self, tag_id: int, with_rooms: bool = False) -> Tag:
        return self.tag_repository.select_tag_by_id(tag_id, with_rooms=with_rooms)
