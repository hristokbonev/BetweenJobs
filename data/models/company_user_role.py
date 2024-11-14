from sqlmodel import SQLModel, Field
from sqlmodel import Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.models.company import Company
    from data.models.user import User
    from data.models.role import Role

class CompanyUserRole(SQLModel, table=True):
    __tablename__ = "CompaniesUsersRoles"

    company_id: int = Field(foreign_key="Companies.id", primary_key=True)
    user_id: int = Field(foreign_key="Users.id", primary_key=True)
    role_id: int = Field(foreign_key="Roles.id", primary_key=True)

    company: "Company" = Relationship(back_populates="roles")
    user: "User" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="users")