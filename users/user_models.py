from datetime import datetime
from pydantic import BaseModel


class UsersResponse(BaseModel):
    '''Used in user get endoiints'''
    id: int | None = None
    username : str
    first_name : str
    last_name : str
    is_admin : bool
    date_of_birth : datetime
    email : str


    class Config:
        orm_mode = True


class UserRegistrationRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    email: str

    class Config:
        orm_mode = True


