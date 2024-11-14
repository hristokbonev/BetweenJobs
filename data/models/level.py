from sqlmodel import SQLModel, Field
from sqlmodel import Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from data.models.skill import Skill
    from data.models.skill_level import SkillLevel


class Level(SQLModel, table=True):
    __tablename__ = "SkillsLevels"

    id: int = Field(primary_key=True, index=True)
    level: int = Field(index=True, unique=True)

    skills: List["Skill"] | None = Relationship(back_populates="levels", link_model=SkillLevel)