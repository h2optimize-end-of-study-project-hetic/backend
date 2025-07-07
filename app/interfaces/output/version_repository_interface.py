from abc import ABC, abstractmethod

from src.domain.entities.version import Version 

class VersionRepositoryInterface(ABC):
    @abstractmethod
    async def get_version(self) -> Version:
        pass


