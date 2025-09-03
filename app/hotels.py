from fastapi import Query, APIRouter, Body

from schemas.hotels import HotelPatch, Hotel

router = APIRouter(prefix='/hotels', tags=["Отели"])

hotels_data = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get('/', summary='Получение данных об отелях')
async def hotels(
    identifier: int | None = Query(description='Идентификатор отеля', default=None, gt=0),
    title: str | None = Query(description='Названия отеля', default=None),
    page: int = Query(description='Номер страницы', default=1, gt=0),
    per_page: int = Query(description='Количество отелей на странице', default=3),
) -> list[dict]:
    hotels_ = []
    global hotels_data
    start = (page - 1) * per_page
    stop = page * per_page

    for hotel in hotels_data:
        if identifier and hotel["id"] != identifier:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if start > len(hotels_):
        hotels_ = []

    return hotels_[start:stop]


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

    if hotel_data.name:
        current_hotel['name'] = hotel_data.name

    return {'status': 'ok', 'id': hotel_id}


@router.post('/', summary='Добавление нового отеля')
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            '1': {'summary': 'Сочи', 'value': {'title': 'sochi', 'name': 'sochi hotel and spa resort'}}
        }
)):
    global hotels_data
    hotels_data.append({
        'id': hotels_data[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name,
    })

    return {'status': 'ok', 'id': hotels_data[-1]['id']}


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
    current_hotel['name'] = hotel_data.name

    return {'status': 'ok', 'id': hotel_id}


@router.delete('/{hotel_id}', summary='Удаление отеля')
async def delete_hotel(hotel_id: int):
    global hotels_data
    d = hotels_data
    hotels_data = [hotel for hotel in d if hotel['id'] != hotel_id]
    return {'status': 'ok'}