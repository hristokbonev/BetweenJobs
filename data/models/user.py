from datetime import datetime
from typing import Optional
from sqlmodel import Relationship
from sqlmodel import SQLModel, Field
from datetime import date
from typing import List
from data.models.jobAd import JobAds
from data.models.resume import Resumes
from data.models.moderator import Moderators


class Users(SQLModel, table=True):
    __tablename__ = "Users"

    id: int = Field(primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    username: str = Field(unique=True, index=True)
    password: str
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    is_admin: bool = Field(default=False)
    date_of_birth: date
    email: str = Field(unique=True, index=True)
    employer_id: int = Field(default=None, foreign_key="Companies.id")

    job_ads: List["JobAds"] = Relationship(back_populates="user")
    resumes: List["Resumes"] = Relationship(back_populates="user")
    moderators: List["Moderators"] = Relationship(back_populates="user")
    
  


