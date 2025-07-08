import asyncpg

from src.domain.entities.version import Version
from src.interfaces.output.version_repository_interface import VersionRepositoryInterface

class PostgresVersionRepository(VersionRepositoryInterface):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_version(self) -> Version:
        row = await self.pool.fetchrow("SELECT name, version FROM version LIMIT 1")
        return Version(name=row["name"], version=row["version"])
