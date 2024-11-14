from sqlmodel import SQLModel, Field
from typing import TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.resume import Resume
    from data.models.job_ad import JobAd

class Match(SQLModel, table=True):
    __tablename__ = "Matches"

    resume_id: int = Field(foreign_key="Resumes.id", primary_key=True)
    jobad_id: int = Field(foreign_key="JobAds.id", primary_key=True)

    resume: "Resume" = Relationship(back_populates="matches")
    job_ad: "JobAd" = Relationship(back_populates="matches")