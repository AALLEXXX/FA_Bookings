from app.exeptions import IncorrenctEmailOrPasswordExeption, UserAlreadyExistsExeption
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.user_model import Users
from app.users.schemas import SUserRegister
from fastapi import APIRouter, Depends,Response



router = APIRouter(
    prefix= "/auth",
    tags=['Auth & Пользователи'],
)

@router.post('/register')
async def register_user(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsExeption
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)

@router.post('/login')
async def login_user(response : Response, 
                     user_data: SUserRegister):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if not user: 
        raise IncorrenctEmailOrPasswordExeption
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user(response : Response):
    response.delete_cookie('booking_access_token')

@router.post('/me')
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user 
 
