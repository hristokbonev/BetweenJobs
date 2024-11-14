from sqlmodel import SQLModel, Field
from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.company import Company
    from data.models.education import Education
    from data.models.employment_type import EmploymentType
    from data.models.location import Location
    from data.models.skill import Skill
    from data.models.resume import Resume
    from data.models.match import Match
    from data.models.jobad_skill import JobAdSkill

    
class JobAd(SQLModel, table=True):
    __tablename__ = "JobAds"

    id: int = Field(primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now, index=True, nullable=False)
    title: str = Field(index=True, nullable=False)
    company_id: int = Field(foreign_key="Companies.id", index=True, nullable=False)
    company_name: str = Field(index=True, nullable=False)
    description: str = Field(default=None)
    education_id: int = Field(foreign_key="Education.id", default=None)
    salary: float = Field(index=True, default=None)
    employment_type_id: int = Field(foreign_key="EmploymentTypes.id", default=None, index=True)
    location_id: int = Field(foreign_key="Locations.id", index=True)

    company: "Company" = Relationship(back_populates="job_ads")
    education: "Education" | None = Relationship(back_populates="job_ads")
    location: "Location" = Relationship(back_populates="job_ads")
    employment_type: "EmploymentType" = Relationship(back_populates="job_ads")
    skills: List["Skill"] | None = Relationship(back_populates="job_ads", link_model=JobAdSkill)
    resumes: List["Resume"] | None = Relationship(back_populates="job_ads", link_model=Match)