from pydantic import BaseModel

from users.user_models import UsersResponse


class CompanyResponse(BaseModel):
    name: str
    description: str
    author_id: int
    employees: list[UsersResponse]

    class Config:
        orm_mode = True


class CreateCompanyRequest(BaseModel):
    name: str
    description: str
    author_id: int

    class Config:
        orm_mode = True