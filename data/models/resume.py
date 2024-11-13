from sqlmodel import SQLModel, Field
from typing import List
from data.models.jobAd import JobAds
from data.models.user import Users
from data.models.match import Matches
from sqlmodel import Relationship



class Resumes(SQLModel, table=True):
    __tablename__ = "Resumes"

    user_id: int = Field(foreign_key="Users.id")
    username: str = Field(index=True)
    full_name: str = Field(index=True, default=None)
    title: str = Field(index=True)
    education_id: int = Field(index=True, default=None, foreign_key="Education.id")
    job_description: str = Field(index=True, default=None)
    skills_id: int = Field(foreign_key="Skills.id", default=None)
    location_id: int = Field(index=True, default=None, foreign_key="Locations.id")
    status_id: int = Field(index=True, foreign_key="Statuses.id")
    employment_type_id: int = Field(foreign_key="EmploymentTypes.id", index=True)
    id: int = Field(primary_key=True, index=True)

    user: Users = Relationship(back_populates="resumes")
    job_ads: List[JobAds] = Relationship(back_populates="applicants")
    matches: List["Matches"] = Relationship(back_populates="resume")