from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels_data = [
    {'id': 1, 'title': 'sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'dubai', 'name': 'dubai'},
]


@app.get('/hotels')
async def hotels(
    identifier: int | None = Query(description='Идентификатор отеля', default=None, gt=0),
    title: str | None = Query(description='Названия отеля', default=None),
) -> list[dict]:
    hotels_ = []
    for hotel in hotels_data:
        if identifier and hotel["id"] != identifier:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@app.post('/hotels')
async def create_hotel(
    title: str = Body(embed=True),
    name: str = Body(embed=True)
):
    global hotels_data
    hotels_data.append({
        'id': hotels_data[-1]['id'] + 1,
        'title': title,
        'name': name,
    })

    return {'status': 'ok', 'id': hotels_data[-1]['id']}


@app.patch('/hotels/{hotel_id: int}')
async def edit_hotel(
    hotel_id: int = Query(description='Идентификатор отеля'),
    title: str | None = Body(embed=True, default=None),
    name: str | None = Body(embed=True, default=None)
):
    global hotels_data
    current_hotel = list(filter(lambda hotel: hotel_id == hotel['id'], hotels_data))

    if not current_hotel:
        return {'status': 'error'}

    current_hotel = current_hotel[0]

    if title:
        current_hotel['title'] = title

    if name:
        current_hotel['name'] = name

    return {'status': 'ok', 'id': hotel_id}


@app.put('/hotels/{hotel_id: int}')
async def update_hotel(
    hotel_id: int = Query(description='Идентификатор отеля'),
    title: str = Body(embed=True),
    name: str = Body(embed=True),
):
    global hotels_data
    current_hotel = list(filter(lambda hotel: hotel_id == hotel['id'], hotels_data))

    if not current_hotel:
        return {'status': 'error'}

    current_hotel = current_hotel[0]

    current_hotel['title'] = title
    current_hotel['name'] = name

    return {'status': 'ok', 'id': hotel_id}


@app.delete('/hotels/{hotel_id: int}')
async def delete_hotel(hotel_id: int):
    global hotels_data
    d = hotels_data
    hotels_data = [hotel for hotel in d if hotel['id'] != hotel_id]
    return {'status': 'ok'}


@app.get('/')
async def func():
    return "hello world!!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)