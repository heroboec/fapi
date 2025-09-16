from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=["Авторизация и аутентификация"])


@router.post('/login')
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    auth_service = AuthService()
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=403, detail='Пользователь с такой почтой не зарегистрирован')

    if not auth_service.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=403, detail='Неверный пароль')

    token = auth_service.create_access_token({'user_id': user.id})
    response.set_cookie('access_token', token)
    return {'status': 'ok', 'access_token': token}


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('access_token')
    return {'status': 'ok'}


@router.post('/register')
async def register_user(db: DBDep, data: UserRequestAdd):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password= hashed_password)
    await db.users.add(new_user_data)
    await db.commit()

    return {'status': 'ok'}


@router.get('/me')
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user
