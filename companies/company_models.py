from pydantic import BaseModel
from typing import Optional
from jobposts.jobpost_models import JobAddResponse
from users.user_models import UsersResponse


class CompanyResponse(BaseModel):
    name: str
    description: Optional[str] = None
    author_id: int
    employees: Optional[list[UsersResponse]] = None
    job_ads: Optional[list[JobAddResponse]] = None

    class Config:
        orm_mode = True


class CreateCompanyRequest(BaseModel):
    name: str
    description: str
    author_id: int

    class Config:
        orm_mode = True


class UpdateCompanyRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    author_id: Optional[int] = None

