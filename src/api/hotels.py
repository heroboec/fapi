from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPatch, Hotel

router = APIRouter(prefix='/hotels', tags=["Отели"])


@router.get('/', summary='Получение данных об отелях')
async def hotels(
    pagination: PaginationDep,
    location: str | None = Query(description='Адрес отеля', default=None),
    title: str | None = Query(description='Названия отеля', default=None),
):
    per_page = pagination.per_page or 4
    offset = (pagination.page - 1) * per_page
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=offset,
        )


@router.post('/', summary='Добавление нового отеля')
async def create_hotel(
    data: Hotel = Body(
        openapi_examples={
            '1': {'summary': 'Сочи', 'value': {'title': 'sochi', 'location': 'sochi hotel and spa resort'}}
        }
)):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session=session).add(data)
        await session.commit()

    return {'status': 'ok', 'data': hotel}


@router.patch('/{hotel_id}', summary='Редактирование отеля')
async def edit_hotel(
    data: HotelPatch,
    location: str | None = Query(description='Адрес отеля', default=None),
    title: str | None = Query(description='Названия отеля', default=None),
):
    async with async_session_maker() as session:
        await HotelsRepository(session=session).update(
            data_model=data,
            location=location,
            title=title,
        )
        await session.commit()

    return {'status': 'ok'}


@router.put('/{hotel_id}', summary='Обновление отеля')
async def update_hotel(
    hotel_id: int,
    data: Hotel,
):
    async with async_session_maker() as session:
        await HotelsRepository(session=session).edit(
            data=data,
            id=hotel_id
        )
        await session.commit()

    return {'status': 'ok'}


@router.delete('/{hotel_id}', summary='Удаление отелей')
async def delete_hotels(
    hotel_id: int,
):
    async with async_session_maker() as session:
        await HotelsRepository(session=session).delete(id=hotel_id)
        await session.commit()

    return {'status': 'ok'}