
from pydantic import BaseModel, Field
# from data.db_models import User
from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    hashed_password: str

    class Config:
        from_attributes = True


class CreateUserRequest(BaseModel):
    username: str
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str


