from sqlmodel import SQLModel, Field
from typing import List, TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.user import User
    from data.models.company import Company

class Role(SQLModel, table=True):
    __tablename__ = "Roles"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(unique=True, index=True)

    users: List["User"] | None = Relationship(back_populates="roles", link_model="CompanyUserRole")
    companies: List["Company"] | None = Relationship(back_populates="roles", link_model="CompanyUserRole")