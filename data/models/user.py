from datetime import date, datetime
from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from data.models.company_user_role import CompanyUserRole


if TYPE_CHECKING:
    from data.models.resume import Resume
    from data.models.role import Role
    from data.models.company import Company


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

    roles: List["Role"] | None = Relationship(back_populates="users", link_model=CompanyUserRole)
    companies: List["Company"] | None = Relationship(back_populates="members", link_model=CompanyUserRole)
    companies_authored: List["Company"] | None = Relationship(back_populates="author")
    resumes: List["Resume"] | None = Relationship(back_populates="user")