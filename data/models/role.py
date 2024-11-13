from sqlmodel import SQLModel, Field
from typing import List
from sqlmodel import Relationship
from data.models.company import Company
from data.models.user import User



class Role(SQLModel, table=True):
    __tablename__ = "Roles"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(unique=True, index=True)


    users: List["User"] = Relationship(back_populates="roles", link_model="CompanyUserRole")
    companies: List["Company"] = Relationship(back_populates="roles", link_model="CompanyUserRole")