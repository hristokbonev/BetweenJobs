from sqlmodel import SQLModel, Field
from typing import List
from data.models.job_ad import JobAd
from sqlmodel import Relationship


class EmploymentType(SQLModel, table=True):
    __tablename__ = "Employment"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(index=True, unique=True, nullable=False)

    job_ads: List[JobAd] = Relationship(back_populates="employment_type")
    resumes: List[JobAd] = Relationship(back_populates="employment_type")