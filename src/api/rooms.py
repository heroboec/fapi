from fastapi import APIRouter, Body
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix='/hotels', tags=["Номера"])


@router.get('/{hotel_id}/rooms', summary='Получение данных об номерах в отеле')
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get('/{hotel_id}/rooms/{room_id}', summary='Получение данных о номере')
async def get_room_info(
    room_id: int,
    hotel_id: int,
):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)

    return {'status': 'ok', 'data': result}


@router.post('/{hotel_id}/rooms', summary='Добавление нового номера')
async def create_room(
    hotel_id: int,
    data: RoomAddRequest = Body(
        openapi_examples={
            '1': {'summary': 'Тестовый номер', 'value': {'title': 'Королевский', 'description': 'Номер с огромной кроватью', 'price': 10, 'quantity': 10}}
        }
)):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session=session).add(room_data)
        await session.commit()

    return {'status': 'ok', 'data': room}


@router.patch('/{hotel_id}/rooms/{room_id}', summary='Редактирование номера')
async def update_room(
    hotel_id: int,
    data: RoomPatchRequest,
    room_id: int,
):
    room_data = RoomPatch(**data.model_dump(exclude_unset=True), hotel_id=hotel_id)
    async with async_session_maker() as session:
        await RoomsRepository(session=session).update(
            data=room_data,
            id=room_id,
            exclude_unset=True,
        )
        await session.commit()

    return {'status': 'ok'}


@router.put('/{hotel_id}/rooms/{room_id}', summary='Обновление номеров')
async def edit_room(
    hotel_id: int,
    room_id: int,
    data: RoomAddRequest,
):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session=session).edit(
            data=room_data,
            id=room_id,
            hotel_id=hotel_id,
        )
        await session.commit()

    return {'status': 'ok'}


@router.delete('/{hotels_id}/rooms/{room_id}', summary='Удаление номеров')
async def delete_room(
    room_id: int,
    hotel_id: int,
):
    async with async_session_maker() as session:
        await RoomsRepository(session=session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {'status': 'ok'}
