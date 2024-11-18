from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UsersResponse(BaseModel):

    id: int | None = None
    # created_at: Optional[datetime]
    username : str
    # password : str = Field()
    first_name : str
    last_name : str
    is_admin : bool
    date_of_birth : date
    email : str


    class Config:
        orm_mode = True
    
class UserRegistrationRequest(BaseModel):
    username: str
    password: str = Field(min=4,)
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_admin: bool
    birth_date: Optional[date]
    email: str


class UserSchema(BaseModel):
    id: Optional[int]
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_admin: bool
    email: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: str
    

class Token(BaseModel):
    access_token: str
    token_type: str

