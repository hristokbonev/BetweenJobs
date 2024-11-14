from sqlmodel import SQLModel, Field
from typing import List, TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.job_ad import JobAd
    from data.models.resume import Resume

class EmploymentType(SQLModel, table=True):
    __tablename__ = "EmploymentTypes"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(index=True, unique=True, nullable=False)

    job_ads: List["JobAd"] = Relationship(back_populates="employment_type")
    resumes: List["Resume"] = Relationship(back_populates="employment_type")