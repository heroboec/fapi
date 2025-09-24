from datetime import date

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import available_rooms_by_date_query
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_date(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = available_rooms_by_date_query(
            date_from,
            date_to,
            hotel_id,
        )

        return self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))

