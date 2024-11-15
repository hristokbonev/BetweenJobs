from datetime import date
from pydantic import BaseModel


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
    password: str
    first_name: str
    last_name: str
    date_of_birth: date
    email: str

    class Config:
        orm_mode = True


