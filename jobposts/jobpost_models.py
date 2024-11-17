from pydantic import BaseModel
from typing import Optional


class CreateJobAdRequest(BaseModel):
    title: str
    company_id: int
    company_name: str
    description: Optional[str]
    education_id: Optional[int]
    salary: Optional[float]
    employment_type_id: Optional[int]
    location_id: Optional[int]

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

    class Config:
        orm_mode = True