from pydantic import Field
from sqlmodel import SQLModel


class ResumeSkill(SQLModel, table=True):
    __tablename__ = "ResumesSkills"

    resume_id: int = Field(foreign_key="Resumes.id", primary_key=True)
    skill_id: int = Field(foreign_key="Skills.id", primary_key=True)

    

    