import datetime
import time
import asyncio
from asyncio import sleep


async def search_routine(query: str) -> str:
    print(f"Получен запрос: {query}")
    if query.lower() == "сочи":
        await sleep(4)
    elif query.lower() == "дубай":
        await sleep(2)
    print(f"Данные получены: {query}")
    return 'готово'


async def main():
    start = time.time()
    # await search_routine('сочи')
    # await search_routine('дубай')
    result = await asyncio.gather(
        search_routine('сочи'),
        search_routine('дубай'),
        return_exceptions=True,
    )
    time_diff = time.time() - start
    print(f'прошло {time_diff} ')
    print(result)

if __name__ == '__main__':
    asyncio.run(main())