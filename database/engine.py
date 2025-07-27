from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker

from database.model import Base_town

engine = create_async_engine("sqlite+aiosqlite:///my_towns.db",echo=True)
session_maker = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=True)

async def create_db():
    async with (engine.begin() as conn):
        await conn.run_sync(Base_town.metadata.create_all)


async def drop_db():
    async with (engine.begin() as conn):
        await conn.run_sync(Base_town.metadata.drop_all)
