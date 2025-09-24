from datetime import date

from sqlalchemy import func, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def available_rooms_by_date_query(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
):
    """
    Формирование запроса на получение идентификаторов номеров, которые свободны в конкретные даты
    с возможностью фильтрации по идентификатору отеля.
    """

    """
    !select room_id, count(*) as rooms_booked from bookings
    	where date_from <= '2024-11-07' and date_to >= '2024-07-01'
    	group by room_id
    """
    rooms_count = select(
        BookingsOrm.room_id,
        func.count(BookingsOrm.id).label('rooms_booked'),
    ).filter(
        BookingsOrm.date_from <= date_to,
        BookingsOrm.date_to >= date_from,
    ).group_by(
        BookingsOrm.room_id,
    ).cte(name='rooms_count')
    """
    !select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
    	from rooms
    	left join rooms_count on rooms.id = rooms_count.room_id
    """
    rooms_left_table = select(
        RoomsOrm.id.label('room_id'),
        (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label('rooms_left'),
    ).join(
        rooms_count,
        rooms_count.c.room_id == RoomsOrm.id,
        isouter=True,
    ).cte(
        name='rooms_left_table',
    )
    """
    !select * from rooms_left_table
    where rooms_left > 0;
    """
    get_rooms_ids_for_hotel = select(
        RoomsOrm.id,
    )

    if hotel_id:
        get_rooms_ids_for_hotel = get_rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    get_rooms_ids_for_hotel = get_rooms_ids_for_hotel.subquery("rooms_ids_for_hotel")

    rooms_ids_to_get = select(
        rooms_left_table.c.room_id,
    ).filter(
        rooms_left_table.c.rooms_left > 0,
        rooms_left_table.c.room_id.in_(get_rooms_ids_for_hotel),
    )

    return rooms_ids_to_get