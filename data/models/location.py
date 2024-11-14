from pydantic import Field
from sqlmodel import SQLModel, Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from data.models.job_ad import JobAd
    from data.models.resume import Resume

class Location(SQLModel, table=True):
    __tablename__ = "Locations"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(index=True, unique=True)

    job_ads: List["JobAd"] = Relationship(back_populates="location")
    resumes: List["Resume"] | None = Relationship(back_populates="location")