from fastapi import APIRouter, HTTPException, Response, Request

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=["Авторизация и аутентификация"])


@router.post('/login')
async def login_user(
    data: UserRequestAdd,
    response: Response,
):
    auth_service = AuthService()
    async with async_session_maker() as session:
        user = await UsersRepository(session=session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=403, detail='Пользователь с такой почтой не зарегистрирован')

        if not auth_service.verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=403, detail='Неверный пароль')

        token = auth_service.create_access_token({'user_id': user.id})
        response.set_cookie('access_token', token)
    return {'status': 'ok', 'access_token': token}


@router.post('/register')
async def register_user(data: UserRequestAdd):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password= hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session=session).add(new_user_data)
        await session.commit()

    return {'status': 'ok'}


@router.get('/only_auth')
async def only_auth(request: Request):
    cookies = request.cookies or {}
    access_token = cookies.get('access_token')
    if access_token:
        result = {'status': 'ok', 't': access_token}
    else:
        result = {'status': 'ok', 'text': 'Токен не найден'}

    return result


