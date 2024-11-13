from sqlmodel import SQLModel, Field
from typing import List
from data.models.moderator import Moderators
from sqlmodel import Relationship



class Roles(SQLModel, table=True):
    __tablename__ = "Roles"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(unique=True, index=True)

    moderators: List[Moderators] = Relationship(back_populates="role")