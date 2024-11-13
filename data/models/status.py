from typing import List
from data.models.resume import Resumes
from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field
from sqlmodel import Relationship


class Statuses(SQLModel, table=True):
    __tablename__ = "Statuses"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(unique=True, index=True)
    
    resumes: List[Resumes] = Relationship(back_populates="status")