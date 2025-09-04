from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(description='Номер страницы', default=1, gt=0)]
    per_page: Annotated[int | None, Query(description='Количество отелей на странице', default=None, gt=0, le=100)]


PaginationDep = Annotated[PaginationParams, Depends()]