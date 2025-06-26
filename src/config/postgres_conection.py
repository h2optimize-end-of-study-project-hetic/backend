import asyncpg

_pg_pool = None

async def get_pg_pool():
    global _pg_pool
    if _pg_pool is None:
        _pg_pool = await asyncpg.create_pool(
            user='postgres',
            password='postgres',
            database='appdb',
            host='localhost',
            port=5432
        )
    return _pg_pool