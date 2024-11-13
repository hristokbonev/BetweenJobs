from sqlmodel import SQLModel, Field
from typing import List
from data.models.resume import Resumes
from sqlmodel import Relationship
from data.models.jobAd import JobAds


class Matches(SQLModel, table=True):
    __tablename__ = "Matches"

    resume_id: int = Field(foreign_key="Resumes.id", primary_key=True)
    job_id: int = Field(foreign_key="JobsAds.id", primary_key=True)

    resume: Resumes = Relationship(back_populates="matches")
    job_ads: JobAds = Relationship(back_populates="matches")