from data.models.resume import Resumes
from sqlmodel import SQLModel, Field
from typing import List
from sqlmodel import Relationship
from data.models.jobad import JobAds


class Skills(SQLModel, table=True):
    __tablename__ = "Skills"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True, index=True)
    skill_level_id: int = Field(foreign_key="SkillLevels.id")

    resumes: List[Resumes] = Relationship(back_populates="skills")
    job_ads: List[JobAds] = Relationship(back_populates="skills")
    