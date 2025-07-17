from app.src.domain.entities.tag import Tag
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.domain.interface_repositories.room_repository import RoomRepository


class CreateTagUseCase:
    def __init__(self, tag_repository: TagRepository, room_repository: RoomRepository):
        self.tag_repository = tag_repository
        self.room_repository = room_repository

    def execute(self, tag: Tag) -> Tag:
        return self.tag_repository.create_tag(tag)
