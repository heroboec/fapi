from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix='/hotels', tags=["Номера"])


@router.get('/{hotel_id}/rooms', summary='Получение данных об номерах в отеле')
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-09-01"),
    date_to: date = Query(example="2025-09-10"),
):
    return await db.rooms.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get('/{hotel_id}/rooms/{room_id}', summary='Получение данных о номере')
async def get_room_info(
    db: DBDep,
    room_id : int,
    hotel_id: int,
):
    result = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

    return {'status': 'ok', 'data': result}


@router.post('/{hotel_id}/rooms', summary='Добавление нового номера')
async def create_room(
    db: DBDep,
    hotel_id: int,
    data: RoomAddRequest = Body(
        openapi_examples={
            '1': {'summary': 'Тестовый номер', 'value': {'title': 'Королевский', 'description': 'Номер с огромной кроватью', 'price': 10, 'quantity': 10}}
        }
)):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    room = await db.rooms.add(room_data)
    await db.commit()

    return {'status': 'ok', 'data': room}


@router.patch('/{hotel_id}/rooms/{room_id}', summary='Редактирование номера')
async def update_room(
    db: DBDep,
    hotel_id: int,
    data: RoomPatchRequest,
    room_id: int,
):
    room_data = RoomPatch(**data.model_dump(exclude_unset=True), hotel_id=hotel_id)
    await db.rooms.update(
        data=room_data,
        id=room_id,
        exclude_unset=True,
    )
    await db.commit()

    return {'status': 'ok'}


@router.put('/{hotel_id}/rooms/{room_id}', summary='Обновление номеров')
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomAddRequest,
):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.edit(
        data=room_data,
        id=room_id,
        hotel_id=hotel_id,
    )
    await db.commit()

    return {'status': 'ok'}


@router.delete('/{hotels_id}/rooms/{room_id}', summary='Удаление номеров')
async def delete_room(
    db: DBDep,
    room_id: int,
    hotel_id: int,
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {'status': 'ok'}
