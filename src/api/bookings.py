from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.rooms import Room

router = APIRouter(prefix='/bookings', tags=["Бронирования"])


@router.post('/', summary='Добавление нового бронирования')
async def create_hotel(
    db: DBDep,
    user_id: UserIdDep,
    data: BookingAddRequest,
):
    room: Room = await db.rooms.get_one_or_none(id=data.room_id)
    if not room:
        raise HTTPException(status_code=401, detail='Указан несуществующий номер')

    booking_data = BookingAdd(user_id=user_id, price=room.price, **data.model_dump())
    booking = await db.bookings.add(booking_data)
    await db.commit()

    return {'status': 'ok', 'data': booking}
