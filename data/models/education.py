from sqlmodel import SQLModel, Field
from typing import List, TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.resume import Resume

class Education(SQLModel, table=True):
    __tablename__ = "Education"

    id: int = Field(primary_key=True, index=True)
    degree_level: str = Field(index=True, unique=True, nullable=False)

    job_ads: List["Resume"] | None = Relationship(back_populates="education")
    resumes: List["Resume"] | None = Relationship(back_populates="education")