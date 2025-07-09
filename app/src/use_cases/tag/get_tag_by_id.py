from app.src.domain.entities.tag import Tag
from app.src.domain.interface_repositories.tag_repository import TagRepository

class GetTagByIdUseCase:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def execute(self, tag_id: int) -> Tag:
        value = self.tag_repository.select_tag_by_id(tag_id)
        print(value)
        
        return value

    # def execute(self, tag_id: int) -> Tag:
    #     return self.tag_repository.select_tag_by_id(tag_id)
    
        # if tag_id  == 0: 
        #     return Tag(id=1, name="Capteur 1", source_address="1126982881", description="Description 1")
        # else :
        #     return

