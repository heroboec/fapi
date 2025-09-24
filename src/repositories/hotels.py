from datetime import date

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

from src.repositories.utils import available_rooms_by_date_query


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
        return [self.schema.model_validate(item, from_attributes=True) for item in result.scalars()]

    async def get_filtered_by_date(
        self,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = available_rooms_by_date_query(
            date_from,
            date_to,
        )

        hotels_ids = select(
            RoomsOrm.hotel_id,
        ).filter(
            RoomsOrm.id.in_(rooms_ids_to_get),
        )

        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids))

