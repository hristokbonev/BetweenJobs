from sqlmodel import SQLModel, Field

class CompanyUserRole(SQLModel, table=True):
    __tablename__ = "CompaniesUsersRoles"

    company_id: int = Field(foreign_key="Companies.id", primary_key=True)
    user_id: int = Field(foreign_key="Users.id", primary_key=True)
    role_id: int = Field(foreign_key="Roles.id", primary_key=True)