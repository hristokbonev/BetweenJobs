from sqlmodel import SQLModel, Field 
from sqlalchemy import Column, Integer, String


class SkillLevels(SQLModel, table=True):
    __tablename__ = "SkillLevels"

    id: int = Field(primary_key=True, index=True)
    level: int = Field(index=True, unique=True)

  