from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, Hotel, HotelAdd

router = APIRouter(prefix='/hotels', tags=["Отели"])


@router.get('/', summary='Получение данных об отелях')
async def hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(description='Адрес отеля', default=None),
    title: str | None = Query(description='Названия отеля', default=None),
):
    per_page = pagination.per_page or 4
    offset = (pagination.page - 1) * per_page

    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=offset,
    )


@router.get('/{hotel_id}', summary='Получение данных об отеле по id')
async def get_hotel(
    db: DBDep,
    hotel_id: int,
):
    result = await db.hotels.get_one_or_none(id=hotel_id)

    return {'status': 'ok', 'data': result}


@router.post('/', summary='Добавление нового отеля')
async def create_hotel(
    db: DBDep,
    data: HotelAdd = Body(
        openapi_examples={
            '1': {'summary': 'Сочи', 'value': {'title': 'sochi', 'location': 'sochi hotel and spa resort'}}
        }
)):
    hotel = await db.hotels.add(data)
    await db.commit()

    return {'status': 'ok', 'data': hotel}


@router.patch('/{hotel_id}', summary='Редактирование отеля')
async def update_hotel(
    db: DBDep,
    data: HotelPatch,
    hotel_id: int,
):
    await db.hotels.update(
        data=data,
        id=hotel_id,
        exclude_unset=True,
    )
    await db.commit()

    return {'status': 'ok'}


@router.put('/{hotel_id}', summary='Обновление отеля')
async def edit_hotel(
    db: DBDep,
    hotel_id: int,
    data: HotelAdd,
):
    await db.hotels.edit(
        data=data,
        id=hotel_id
    )
    await db.commit()

    return {'status': 'ok'}


@router.delete('/{hotel_id}', summary='Удаление отелей')
async def delete_hotels(
    db: DBDep,
    hotel_id: int,
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {'status': 'ok'}
