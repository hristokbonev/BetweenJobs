from sqlmodel import SQLModel, Field
from typing import List
from data.models.company import Companies
from data.models.user import Users
from data.models.role import Roles
from sqlmodel import Relationship



class Moderators(SQLModel, table=True):
    __tablename__ = "Moderators"

    company_id: int = Field(foreign_key="Companies.id", primary_key=True)
    user_id: int = Field(foreign_key="Users.id", primary_key=True)
    role_id: int = Field(foreign_key="Roles.id", primary_key=True)

    company: Companies = Relationship(back_populates="moderators")
    user: Users = Relationship(back_populates="moderators")
    role: "Roles" = Relationship(back_populates="moderators")