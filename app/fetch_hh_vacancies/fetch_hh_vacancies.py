import requests
from time import sleep
import json
from dataclasses import dataclass, asdict

url = 'https://api.hh.ru/vacancies'

@dataclass(repr=True)
class VacancyData:
    salary_max: int | None
    salary_min: int | None
    salary_currency: str | None
    title: str
    link: str
    job: str


def retry(retry_count: int = 3, sleep_interval: int = 2):
    def wrapper(func):
        def inner(*args, **kwargs):
            try_number = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if try_number < retry_count - 1:
                        try_number += 1
                        sleep(sleep_interval)
                    else:
                        raise
        return inner
    return wrapper


@retry()
def fetch_hh_vacancies(url: str, page: int = 0) -> list[VacancyData]:
    params = {
        'test': 'fastapi OR django OR flask',
        'per_page': 100,
        'page': page,
    }

    resp = requests.get(
        url,
        params=params,
    )

    if resp.status_code != 200:
        raise Exception('Получен статус отличный от 200')

    vacancies = resp.json()['items'] or []
    result = []
    for vacancy in vacancies:
        salary = vacancy.get('salaty') or {}
        min = salary.get('from')
        max = salary.get('to')
        currency = salary.get('currency')

        v = VacancyData(
            salary_max=max,
            salary_min=min,
            salary_currency=currency,
            title=vacancy.get('name', ''),
            link=vacancy.get('url', ''),
            job=', '.join([role['name'] for role in vacancy.get('professional_roles', [])])
        )
        result.append(v)

    return result


def fetch_all_vacancies():
    page = 0
    result = []
    while True:
        print(f'Fetch {page} page...')
        if page == 5:
            break
        current_batch = fetch_hh_vacancies(url, page)
        sleep(1)
        if len(current_batch) == 0:
            break
        result.extend(current_batch)
        page += 1

    with open("vacancies.json", "w", encoding="utf-8") as f:
        json.dump([asdict(v) for v in result], f, ensure_ascii=False, indent=2)


def main():
    print(fetch_all_vacancies())


if __name__ == "__main__":
    main()