from pydantic import Field
from sqlmodel import SQLModel


class JobAdSkill(SQLModel, table=True):

    __tablename__ = "JobAdsSkills"

    jobad_id: int = Field(foreign_key="JobAds.id", primary_key=True)
    skill_id: int = Field(foreign_key="Skills.id", primary_key=True)

