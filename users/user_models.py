from datetime import datetime
from pydantic import BaseModel, Field, root_validator


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


class CreateSkillRequest(BaseModel):
    skill_name: str
    is_scalable: bool = False
    level: int = Field(None, ge=1, le=3, description="Level must be between 1 and 3")

    @root_validator
    def validate_level(cls, values):
        is_scalable = values.get('is_scalable')
        level = values.get('level')
        if is_scalable and level is None:
            raise ValueError("Level is required when is_scalable is True.")
        if not is_scalable and level is not None:
            raise ValueError("Level cannot be provided when is_scalable is False.")
        return values

    class Config:
        orm_mode = True