from pydantic import BaseModel, EmailStr


class SUserRegister(BaseModel):
    email: EmailStr
    password: str

class SUserMe(BaseModel):
    email: EmailStr
