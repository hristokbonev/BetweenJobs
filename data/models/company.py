from sqlmodel import SQLModel, Field
from sqlalchemy import TIMESTAMP
from typing import List
from sqlmodel import Relationship
from data.models.jobad import JobAds
from data.models.moderator import Moderators
from data.models.user import Users


class Companies(SQLModel, table=True):
    __tablename__ = "Companies"

    id: int = Field(primary_key=True, index=True)
    created_at: str = TIMESTAMP(nullable=False, server_default="now()")
    name: str = Field(index=True, nullable=False)
    description: str = Field(default=None)
    author_id: int = Field(nullable=False, index=True, foreign_key="Users.id")

    job_ads: List["JobAds"] = Relationship(back_populates="company")
    moderators: List["Moderators"] = Relationship(back_populates="company")
    employees: List["Users"] = Relationship(back_populates="employer")