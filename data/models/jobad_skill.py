from sqlmodel import SQLModel, Field
from typing import TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.job_ad import JobAd
    from data.models.skill import Skill

class JobAdSkill(SQLModel, table=True):
    __tablename__ = "JobAdsSkills"

    jobad_id: int = Field(foreign_key="JobAds.id", primary_key=True)
    skill_id: int = Field(foreign_key="Skills.id", primary_key=True)

    job_ad: "JobAd" = Relationship(back_populates="skills")
    skill: "Skill" = Relationship(back_populates="job_ads")