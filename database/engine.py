from sqlalchemy import MetaData, URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine as create_async_engine_


def create_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine_(url, future=True)


async def init_tables(engine: AsyncEngine, metadata: MetaData):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
