from typing import List
from data.models.resume import Resume
from sqlmodel import SQLModel, Field
from sqlmodel import Relationship


class Status(SQLModel, table=True):
    __tablename__ = "Statuses"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(unique=True, index=True)
    
    resumes: List[Resume] = Relationship(back_populates="status")
    job_ads: List[Resume] = Relationship(back_populates="status")