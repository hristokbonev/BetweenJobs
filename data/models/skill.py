from sqlmodel import SQLModel, Field
from typing import List, TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.level import Level
    from data.models.job_ad import JobAd
    from data.models.resume import Resume
    from data.models.skill_level import SkillLevel
    from data.models.jobad_skill import JobAdSkill
    from data.models.resume_skill import ResumeSkill

class Skill(SQLModel, table=True):
    __tablename__ = "Skills"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True, index=True)
    skill_level_id: int = Field(foreign_key="SkillLevels.id")

    levels: List["Level"] | None = Relationship(back_populates="skills", link_model=SkillLevel)
    job_ads: List["JobAd"] | None = Relationship(back_populates="skills", link_model=JobAdSkill)
    resumes: List["Resume"] | None = Relationship(back_populates="skills", link_model=ResumeSkill)