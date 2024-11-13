from datetime import datetime
from sqlmodel import Relationship
from sqlmodel import SQLModel, Field
from datetime import date
from typing import List
from data.models.resume import Resume
from data.models.company import Company
from data.models.role import Role


class User(SQLModel, table=True):
    __tablename__ = "Users"

    id: int = Field(primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    username: str = Field(unique=True, index=True)
    password: str
    first_name: str = Field
    last_name: str = Field
    is_admin: bool = Field(default=False)
    date_of_birth: date
    email: str = Field(unique=True, index=True)
    employer_id: int = Field(default=None, foreign_key="Companies.id")

    roles: List["Role"] = Relationship(back_populates="users", link_model="CompanyUserRole")
    companies: List["Company"] = Relationship(back_populates="users", link_model="CompanyUserRole")
    companies_authored: List["Company"] = Relationship(back_populates="author")
    resumes: List[Resume] = Relationship(back_populates="user")
    
    


