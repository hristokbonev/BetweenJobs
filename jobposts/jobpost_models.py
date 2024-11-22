from datetime import datetime
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

class JobAdResponseWithNamesNotId(BaseModel):
    title: str
    created_at: datetime
    company_name: str
    description: str | None = None
    education: str | None = None
    salary: float
    employment: str
    location: str
    status: str | None = None
    skills: list[str] | None = None

    class Config:
        orm_mode = True

class JobAdResponseWithSkills(BaseModel):

    id: int
    title: str
    created_at: datetime
    company_name: str
    description: str | None = None
    education: int | None = None
    salary: float
    employment: int
    location: int
    status: int | None = None
    skills: list[int] | None = None

    class Config:
        orm_mode = True