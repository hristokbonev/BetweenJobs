from datetime import datetime
from typing import Optional
from sqlalchemy import TIMESTAMP
from sqlmodel import SQLModel, Field


class JobAds(SQLModel, table=True):
    __tablename__ = "jobs"


    id : int = Field(default=None, primary_key=True)
    created_ad :  Optional[datetime] = Field(default_factory=datetime.now)
    title : str = Field(index=True)
    company_id : int = Field(foreign_key="companies.id")
    company_name : str = Field(index=True)
    description : str = Field(index=True)
    skill_id : int = Field(foreign_key="skills.id")
    education_id : int = Field(foreign_key="education.id")
    employment : str = Field(index=True)
    salary : float = Field(index=True)
    employment_type_id : int = Field(foreign_key="employment.id")

