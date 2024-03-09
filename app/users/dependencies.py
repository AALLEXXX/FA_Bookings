from datetime import datetime
from app.config import settings
from app.exeptions import IncorrenctTokenFormatExeption, TokenAbsentExeption, TokenExpiredExeption, UserIsNotPresentExeption
from app.users.dao import UserDAO
from fastapi import Depends, Request
from jose import jwt, JWSError

def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentExeption
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
        token, settings.SECRET_KEY, settings.ALGORITHM
    )   
    except JWSError:
        raise IncorrenctTokenFormatExeption
    
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredExeption
    
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentExeption
    
    user = await UserDAO.find_by_id(int(user_id))
    if not user: 
        raise UserIsNotPresentExeption
    return user
