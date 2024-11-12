from datetime import datetime
from typing import Optional
from sqlmodel import Relationship
from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True, index=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    username : str = Field(unique=True, index=True)
    password : str = Field()
    first_name : str = Field()
    last_name : str = Field()
    is_admin : bool = Field(default=False)
    date_of_birth : str = Field()
    email : str = Field(unique=True, index=True)

    job_ads: Relationship = Relationship(back_populates="users")
    resumes: Relationship = Relationship(back_populates="users")
    
  


