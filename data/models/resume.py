from sqlmodel import SQLModel, Field
from typing import List, TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from data.models.job_ad import JobAd
    from data.models.employment_type import EmploymentType
    from data.models.location import Location
    from data.models.status import Status
    from data.models.skill import Skill
    from data.models.education import Education
    from data.models.user import User
    from data.models.match import Match
    from data.models.resume_skill import ResumeSkill

class Resume(SQLModel, table=True):
    __tablename__ = "Resumes"

    user_id: int = Field(foreign_key="Users.id")
    username: str = Field(index=True)
    full_name: str = Field(index=True, default=None)
    title: str = Field(index=True)
    education_id: int = Field(index=True, default=None, foreign_key="Education.id")
    summary: str = Field(index=True, default=None)
    location_id: int = Field(index=True, default=None, foreign_key="Locations.id")
    status_id: int = Field(index=True, foreign_key="Statuses.id")
    employment_type_id: int = Field(foreign_key="EmploymentTypes.id", index=True)
    id: int = Field(primary_key=True, index=True)

    user: "User" = Relationship(back_populates="resumes")
    job_ads: List["JobAd"] | None = Relationship(back_populates="resumes", link_model=Match)
    skills: List["Skill"] | None = Relationship(back_populates="resumes", link_model=ResumeSkill)
    education: "Education" = Relationship(back_populates="resumes")
    location: "Location" = Relationship(back_populates="resumes")
    status: "Status" = Relationship(back_populates="resumes")
    employment_type: "EmploymentType" = Relationship(back_populates="resumes")