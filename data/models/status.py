from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.resume import Resume
    from data.models.job_ad import JobAd

class Status(SQLModel, table=True):
    __tablename__ = "Statuses"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(unique=True, index=True)
    
    resumes: List["Resume"] | None = Relationship(back_populates="status")
    job_ads: List["JobAd"] | None = Relationship(back_populates="status")