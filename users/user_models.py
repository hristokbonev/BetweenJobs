from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):

    id: int | None = None
    username : str
    first_name : str
    last_name : str
    is_admin : bool
    date_of_birth : date
    email : str

    class Config:
        from_attributes = True


class UsersResponse(BaseModel):
    '''Used in user get endoiints'''
    id: int | None = None
    # created_at: Optional[datetime] = Field(default_factory=datetime.now)
    username : str
    # password : str = Field()
    first_name : str
    last_name : str
    is_admin : bool
    date_of_birth : date
    email : str


    class Config:
        from_attributes = True
    
class UserRegistrationRequest(BaseModel):
    username: str
    password: str = Field(min=4,)
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_admin: bool
    birth_date: Optional[date]
    email: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    new_password: Optional[str] = None
    confirm_password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class UserSchema(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_admin: bool 
    email: Optional[str] =  None


class CreateSkillRequest(BaseModel):
    name: str
    is_scalable: bool = False

    class Config:
        orm_mode = True
class TokenData(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserSearch(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None



class ResetPasswordRequest(BaseModel):
    username: str
    new_password: str
    confirm_password: str
