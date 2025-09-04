from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.config import settings
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

# raw query example
# async def func():
#     async with engine.begin() as conn:
#         res = await conn.execute(text('select version()'))
#         print(res.fetchone())
#
# asyncio.run(func())