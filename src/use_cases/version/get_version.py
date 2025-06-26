from src.interfaces import VersionRepository

class GetVersion:
    def __init__(self, repository: VersionRepository):
        self.repository = repository

    async def execute(self):
        return await self.repository.get_version()