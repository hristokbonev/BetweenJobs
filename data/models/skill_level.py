from sqlmodel import SQLModel
from sqlmodel import Field



class SkillLevel(SQLModel, table=True):
    __tablename__ = "SkillsLevels"

    skill_id: int = Field(primary_key=True, index=True, foreign_key="Skills.id")
    level_id: int = Field(primary_key=True, index=True, foreign_key="Levels.id")
