from sqlmodel import SQLModel, Field
from sqlmodel import Relationship
from typing import List
from data.models.skill import Skill


class Level(SQLModel, table=True):
    __tablename__ = "SkillsLevels"

    id: int = Field(primary_key=True, index=True)
    level: int = Field(index=True, unique=True)

    skills: List[Skill] | None = Relationship(back_populates="levels", link_model="SkillLevel")


  