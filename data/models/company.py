from sqlmodel import SQLModel, Field
from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.role import Role
    from data.models.user import User
    from data.models.job_ad import JobAd
    from data.models.company_user_role import CompanyUserRole

class Company(SQLModel, table=True):
    __tablename__ = "Companies"

    id: int = Field(primary_key=True, index=True)
    created_at: datetime = Field(nullable=False, server_default="now()")
    name: str = Field(index=True, nullable=False)
    description: str = Field(default=None)
    author_id: int = Field(nullable=False, index=True, foreign_key="Users.id")

    roles: List["Role"] | None = Relationship(back_populates="companies", link_model=CompanyUserRole)
    members: List["User"] | None = Relationship(back_populates="companies", link_model=CompanyUserRole)
    author: "User" = Relationship(back_populates="companies_authored")
    job_ads: List["JobAd"] | None = Relationship(back_populates="company")