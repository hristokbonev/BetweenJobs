from sqlmodel import SQLModel, Field
from typing import List
from data.models.resume import Resume
from sqlmodel import Relationship



class Education(SQLModel, table=True):
    __tablename__ = "Education"

    id: int = Field(primary_key=True, index=True)
    degree_level: str = Field(index=True, unique=True, nullable=False)

    job_ads: List[Resume] | None = Relationship(back_populates="education")
    resumes: List[Resume] | None = Relationship(back_populates="education")
    