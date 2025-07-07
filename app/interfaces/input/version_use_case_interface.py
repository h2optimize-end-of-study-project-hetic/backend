from typing import List
from abc import ABC, abstractmethod

from src.domain.entities.version import Version

class GetVersionInterface(ABC):
    @abstractmethod
    def get_version(self) -> Version | None:
        pass
