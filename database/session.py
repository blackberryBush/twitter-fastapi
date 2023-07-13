from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class SessionScope:
    _sessionmaker: async_sessionmaker[AsyncSession] | None = None

    @staticmethod
    def init(sessionmaker: async_sessionmaker[AsyncSession]):
        __class__._sessionmaker = sessionmaker

    @staticmethod
    @asynccontextmanager
    async def get_session() -> AsyncSession:
        async with __class__._sessionmaker() as session:
            session: AsyncSession
            try:
                yield session
            except:
                await session.rollback()
                raise
            finally:
                await session.close()
