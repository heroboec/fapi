from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated
from fastapi import Request, HTTPException

from src.services.auth_service import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(description='Номер страницы', default=1, gt=0)]
    per_page: Annotated[int | None, Query(description='Количество отелей на странице', default=None, gt=0, le=100)]


PaginationDep = Annotated[PaginationParams, Depends()]


async def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail='Вы не предоставили токен доступа')
    return token


async def get_current_user_id(token: str = Depends(get_token)):
    decoded_token = AuthService().decode_token(token)
    user_id = decoded_token.get('user_id')
    if not user_id:
        raise HTTPException(status_code=401, detail='Идентификатор пользователя не найден')

    return user_id

UserIdDep = Annotated[int, Depends(get_current_user_id)]
