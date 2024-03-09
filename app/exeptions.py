from typing import Optional
from fastapi import HTTPException, status


class UserAlreadyExistsExeption(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail='Пользователь уже существует'
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class IncorrenctEmailOrPasswordExeption(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail='Неверная почта или пароль'
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)
        
class TokenExpiredExeption(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail='Токен истек'
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)
        

class TokenAbsentExeption(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail='Токен отсутствует'
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)

class IncorrenctTokenFormatExeption(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail='Неверный формат токена'
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)

class UserIsNotPresentExeption(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ""
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class RoomCannotBeBooked(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных комнат"
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)