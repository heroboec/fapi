from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPatch, Hotel
from sqlalchemy import insert, select, func

router = APIRouter(prefix='/hotels', tags=["Отели"])


@router.get('/', summary='Получение данных об отелях')
async def hotels(
    pagination: PaginationDep,
    location: str | None = Query(description='Адрес отеля', default=None),
    title: str | None = Query(description='Названия отеля', default=None),
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all()

    # per_page = pagination.per_page or 4
    # offset = (pagination.page - 1) * per_page
    # async with async_session_maker() as session:
    #     query = select(HotelsOrm)
    #     if location:
    #         query = query.filter(func.lower(HotelsOrm.location).contains(location.lower()))
    #
    #     if title:
    #         query = query.filter(func.lower(HotelsOrm.title).contains(title.lower()))
    #
    #     query = query.limit(
    #         per_page,
    #     ).offset(
    #         offset,
    #     )
    #     print(query.compile(compile_kwargs={'literal_binds': True}))
    #     result = await session.execute(query)
    #     hotels = result.scalars().all()
    #     return hotels


@router.post('/', summary='Добавление нового отеля')
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            '1': {'summary': 'Сочи', 'value': {'title': 'sochi', 'location': 'sochi hotel and spa resort'}}
        }
)):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {'status': 'ok'}


@router.patch('/{hotel_id}', summary='Редактирование отеля')
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
):
    global hotels_data
    current_hotel = list(filter(lambda hotel: hotel_id == hotel['id'], hotels_data))

    if not current_hotel:
        return {'status': 'error'}

    current_hotel = current_hotel[0]

    if hotel_data.title:
        current_hotel['title'] = hotel_data.title

    if hotel_data.location:
        current_hotel['location'] = hotel_data.location

    return {'status': 'ok', 'id': hotel_id}


@router.put('/{hotel_id}', summary='Обновление отеля')
async def update_hotel(
    hotel_id: int,
    hotel_data: Hotel,
):
    global hotels_data
    current_hotel = list(filter(lambda hotel: hotel_id == hotel['id'], hotels_data))

    if not current_hotel:
        return {'status': 'error'}

    current_hotel = current_hotel[0]

    current_hotel['title'] = hotel_data.title
    current_hotel['location'] = hotel_data.location

    return {'status': 'ok', 'id': hotel_id}


@router.delete('/{hotel_id}', summary='Удаление отеля')
async def delete_hotel(hotel_id: int):
    global hotels_data
    d = hotels_data
    hotels_data = [hotel for hotel in d if hotel['id'] != hotel_id]
    return {'status': 'ok'}