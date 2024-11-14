from pydantic import Field
from sqlmodel import SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.models.resume import Resume
    from data.models.skill import Skill

class ResumeSkill(SQLModel, table=True):
    __tablename__ = "ResumesSkills"

    resume_id: int = Field(foreign_key="Resumes.id", primary_key=True)
    skill_id: int = Field(foreign_key="Skills.id", primary_key=True)

    resume: "Resume" = Relationship(back_populates="skills")
    skill: "Skill" = Relationship(back_populates="resumes")