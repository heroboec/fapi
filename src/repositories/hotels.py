from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
        self,
        location: str,
        title: str,
        limit: int,
        offset: int,
    ):
        # from src.database import engine
        # print(add_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower()))

        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower()))

        query = query.limit(
            limit,
        ).offset(
            offset,
        )

        result = await self.session.execute(query)
        hotels = result.scalars().all()
        return hotels
