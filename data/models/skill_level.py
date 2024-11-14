from sqlmodel import SQLModel, Field
from typing import TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.skill import Skill
    from data.models.level import Level

class SkillLevel(SQLModel, table=True):
    __tablename__ = "SkillsLevels"

    skill_id: int = Field(primary_key=True, index=True, foreign_key="Skills.id")
    level_id: int = Field(primary_key=True, index=True, foreign_key="Levels.id")

    skill: "Skill" = Relationship(back_populates="levels")
    level: "Level" = Relationship(back_populates="skills")