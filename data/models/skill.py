from data.models.resume import Resume
from sqlmodel import SQLModel, Field
from typing import List
from sqlmodel import Relationship
from data.models.job_ad import JobAd
from data.models.level import Level


class Skill(SQLModel, table=True):
    __tablename__ = "Skills"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True, index=True)
    skill_level_id: int = Field(foreign_key="SkillLevels.id")

    levels: List[Level] = Relationship(back_populates="skills", link_model="SkillLevel")
    job_ads: List[JobAd] = Relationship(back_populates="skills", link_model="JobAdSkill")
    resumes: List[Resume] = Relationship(back_populates="skills", link_model="ResumeSkill")