from datetime import datetime
from data.models.company import Company
from sqlmodel import SQLModel, Field
from typing import List
from sqlmodel import Relationship
from data.models.education import Education
from data.models.employment_type import EmploymentType
from data.models.location import Location
from data.models.skill import Skill
from data.models.resume import Resume


class JobAd(SQLModel, table=True):
    __tablename__ = "JobAds"


    id: int = Field(primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now(), index=True, nullable=False)
    title: str = Field(index=True, nullable=False)
    company_id: int = Field(foreign_key="Companies.id", index=True, nullable=False)
    company_name: str = Field(index=True, nullable=False)
    description: str = Field(default=None)
    education_id: int = Field(foreign_key="Education.id", default=None)
    salary: float = Field(index=True, default=None)
    employment_type_id: int = Field(foreign_key="EmploymentTypes.id", default=None, index=True)
    location_id: int = Field(foreign_key="Locations.id", index=True)

    company: Company = Relationship(back_populates="job_ads")
    education: Education = Relationship(back_populates="job_ads")
    location: Location = Relationship(back_populates="job_ads")
    employment_type: EmploymentType = Relationship(back_populates="job_ads")
    skills: List["Skill"] = Relationship(back_populates="job_ads", link_model="JobAdSkill")
    resumes: List["Resume"] = Relationship(back_populates="job_ads", link_model="JobAdResume")
