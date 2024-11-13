from sqlmodel import SQLModel, Field
from typing import List
from data.models.jobAd import JobAds
from sqlmodel import Relationship


class EmploymentTypes(SQLModel, table=True):
    __tablename__ = "Employment"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(index=True, unique=True, nullable=False)

    job_ads: List[JobAds] = Relationship(back_populates="employment_type")