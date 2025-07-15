from app.src.domain.entities.tag import Tag
from app.src.common.exception import AlreadyExistsError
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.domain.interface_repositories.room_repository import RoomRepository


class CreateTagUseCase:
    def __init__(self, tag_repository: TagRepository, room_repository: RoomRepository):
        self.tag_repository = tag_repository
        self.room_repository = room_repository

    def execute(self, tag: Tag, room_id: int | None) -> Tag:
        if self.tag_repository.select_tag_by_src_address(tag.source_address):
            raise AlreadyExistsError("Tag", "source_address", tag.source_address)

        # if room_id and not self.room_repository.select_room_by_id(room_id):
        #     raise NotFoundException('Room', room_id)

        return self.tag_repository.create_tag(tag)
