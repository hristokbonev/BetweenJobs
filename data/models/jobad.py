from datetime import datetime
from typing import Optional
from data.models.company import Companies
from sqlalchemy import TIMESTAMP
from sqlmodel import SQLModel, Field
from typing import List
from sqlmodel import Relationship
from data.models.resume import Resumes
from data.models.match import Matches


class JobAds(SQLModel, table=True):
    __tablename__ = "JobsAds"


    id: int = Field(primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now(), index=True, nullable=False)
    title: str = Field(index=True, nullable=False)
    company_id: int = Field(foreign_key="Companies.id", index=True, nullable=False)
    company_name: str = Field(index=True, nullable=False)
    description: str = Field(default=None)
    skill_id: int = Field(foreign_key="Skills.id", default=None)
    education_id: int = Field(foreign_key="Education.id", default=None)
    salary: float = Field(index=True, default=None)
    employment_type_id: int = Field(foreign_key="EmploymentTypes.id", default=None, index=True)
    location_id: int = Field(foreign_key="Locations.id", default=None)

    company: Companies = Relationship(back_populates="job_ads")
    applicants: List["Resumes"] = Relationship(back_populates="job_ads")
    matches: List["Matches"] = Relationship(back_populates="job_ads")
