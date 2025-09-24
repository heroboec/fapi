from datetime import date

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

from src.repositories.utils import available_rooms_by_date_query
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_date(
        self,
        date_from: date,
        date_to: date,
        limit: int,
        offset: int,
        title: str | None = None,
        location: str | None = None,
    ) -> list[Hotel]:
        rooms_ids_to_get = available_rooms_by_date_query(
            date_from,
            date_to,
        )

        hotels_ids = select(
            RoomsOrm.hotel_id,
        ).filter(
            RoomsOrm.id.in_(rooms_ids_to_get),
        ).subquery("available_hotels_ids")

        hotels_query = select(
            self.model,
        ).filter(self.model.id.in_(hotels_ids))

        if location:
            hotels_query = hotels_query.filter(func.lower(HotelsOrm.location).contains(location.lower()))

        if title:
            hotels_query = hotels_query.filter(func.lower(HotelsOrm.title).contains(title.lower()))

        hotels_query = hotels_query.limit(
            limit,
        ).offset(
            offset,
        )

        result = await self.session.execute(hotels_query)

        return [self.schema.model_validate(item, from_attributes=True) for item in result.scalars()]

