from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker

import database.tables
from database.base import Base
from database.engine import init_tables, create_async_engine
from database.session import SessionScope


async def init_db(url: URL | str):
    async_engine = create_async_engine(url)
    SessionScope.init(async_sessionmaker(async_engine, expire_on_commit=False))
    await init_tables(async_engine, Base.metadata)
