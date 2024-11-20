from pydantic import BaseModel
from typing import Optional


class JobAddResponse(BaseModel):
    title: str
    company_name: str
    company_description: Optional[str] = None
    education: str
    salary: float
    employment: str
    location: str
    status: str

    class Config:
        orm_mode = True


class CreateJobAdRequest(BaseModel):
    title: str
    company_id: int
    company_name: str
    description: Optional[str]
    education_id: Optional[int]
    salary: Optional[float]
    employment_type_id: Optional[int]
    location_id: Optional[int]
    status_id: int = 1
    skill_ids: list[int]

    class Config:
        orm_mode = True


class UpdateJobAdRequest(BaseModel):
    title: Optional[str]
    company_id: Optional[int]
    company_name: Optional[str]
    description: Optional[str]
    education_id: Optional[int]
    salary: Optional[float]
    employment_type_id: Optional[int]
    location_id: Optional[int]
    status_id: Optional[int] = 1
    skill_ids: list[int]

    class Config:
        orm_mode = True