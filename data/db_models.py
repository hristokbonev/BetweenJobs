from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import func


class Location(SQLModel, table=True):
    __tablename__ = "Locations"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(index=True, unique=True)

    job_ads: List["JobAd"] = Relationship(back_populates="location")
    resumes: List["Resume"] = Relationship(back_populates="location")


class Status(SQLModel, table=True):
    __tablename__ = "Statuses"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(unique=True, index=True)

    resumes: List["Resume"] = Relationship(back_populates="status")
    job_ads: List["JobAd"] = Relationship(back_populates="status")


class CompanyUserRole(SQLModel, table=True):
    __tablename__ = "CompaniesUsersRoles"

    company_id: int = Field(foreign_key="Companies.id", primary_key=True)
    user_id: int = Field(foreign_key="Users.id", primary_key=True)
    role_id: int = Field(foreign_key="Roles.id", primary_key=True)


class Company(SQLModel, table=True):
    __tablename__ = "Companies"

    id: int = Field(primary_key=True, index=True)
    created_at: datetime = Field(nullable=False, default=func.now())
    name: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(default=None)
    author_id: int = Field(foreign_key="Users.id")

    members: List["User"] = Relationship(back_populates="companies", link_model=CompanyUserRole)
    roles: List["Role"] = Relationship(back_populates="companies", link_model=CompanyUserRole)
    job_ads: List["JobAd"] = Relationship(back_populates="company")
    author: "User" = Relationship(back_populates="companies_authored")


class User(SQLModel, table=True):
    __tablename__ = "Users"

    id: Optional[int] = Field(primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    username: str = Field(unique=True, index=True)
    password: str
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    is_admin: bool = Field(default=False)
    date_of_birth: date
    email: str = Field(unique=True, index=True)
    employer_id: Optional[int] = Field(default=None)

    roles: List["Role"] = Relationship(back_populates="users", link_model=CompanyUserRole)
    companies: List["Company"] = Relationship(back_populates="members", link_model=CompanyUserRole)
    companies_authored: List["Company"] = Relationship(back_populates="author")
    resumes: List["Resume"] = Relationship(back_populates="user")


class SkillLevel(SQLModel, table=True):
    __tablename__ = "SkillsLevels"

    skill_id: int = Field(primary_key=True, index=True, foreign_key="Skills.id")
    level_id: int = Field(primary_key=True, index=True, foreign_key="Levels.id")


class JobAdSkill(SQLModel, table=True):
    __tablename__ = "JobAdsSkills"

    jobad_id: int = Field(foreign_key="JobAds.id", primary_key=True)
    skill_id: int = Field(foreign_key="Skills.id", primary_key=True)


class ResumeSkill(SQLModel, table=True):
    __tablename__ = "ResumesSkills"

    resume_id: int = Field(foreign_key="Resumes.id", primary_key=True)
    skill_id: int = Field(foreign_key="Skills.id", primary_key=True)


class Skill(SQLModel, table=True):
    __tablename__ = "Skills"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True, index=True)
    is_scalable: bool = Field(default=False)

    levels: List["Level"] = Relationship(back_populates="skills", link_model=SkillLevel)
    job_ads: List["JobAd"] = Relationship(back_populates="skills", link_model=JobAdSkill)
    resumes: List["Resume"] = Relationship(back_populates="skills", link_model=ResumeSkill)


class Role(SQLModel, table=True):
    __tablename__ = "Roles"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(unique=True, index=True)

    users: List["User"] = Relationship(back_populates="roles", link_model=CompanyUserRole)
    companies: List["Company"] = Relationship(back_populates="roles", link_model=CompanyUserRole)


class Match(SQLModel, table=True):
    __tablename__ = "Matches"

    resume_id: int = Field(foreign_key="Resumes.id", primary_key=True)
    jobad_id: int = Field(foreign_key="JobAds.id", primary_key=True)


class Resume(SQLModel, table=True):
    __tablename__ = "Resumes"

    user_id: int = Field(foreign_key="Users.id")
    full_name: Optional[str] = Field(default=None, index=True)
    title: str = Field(index=True)
    education_id: Optional[int] = Field(default=None, foreign_key="Education.id")
    summary: Optional[str] = Field(default=None, index=True)
    location_id: Optional[int] = Field(default=None, foreign_key="Locations.id")
    status_id: int = Field(index=True, foreign_key="Statuses.id", default=1)
    employment_type_id: int = Field(foreign_key="EmploymentTypes.id", index=True)
    id: int = Field(primary_key=True, index=True)


    user: "User" = Relationship(back_populates="resumes")
    job_ads: List["JobAd"] = Relationship(back_populates="resumes", link_model=Match)
    skills: List["Skill"] = Relationship(back_populates="resumes", link_model=ResumeSkill)
    education: "Education" = Relationship(back_populates="resumes")
    location: Optional[Location] = Relationship(back_populates="resumes")
    status: "Status" = Relationship(back_populates="resumes")
    employment_type: "EmploymentType" = Relationship(back_populates="resumes")


class Level(SQLModel, table=True):
    __tablename__ = "Levels"

    id: int = Field(primary_key=True, index=True)
    level: int = Field(index=True, unique=True)

    skills: List["Skill"] = Relationship(back_populates="levels", link_model=SkillLevel)


class JobAd(SQLModel, table=True):
    __tablename__ = "JobAds"

    id: int = Field(primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now, index=True, nullable=False)
    title: str = Field(index=True, nullable=False)
    company_id: int = Field(foreign_key="Companies.id", index=True, nullable=False)
    company_name: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(default=None)
    education_id: Optional[int] = Field(foreign_key="Education.id", default=None)
    salary: Optional[float] = Field(default=None, index=True)
    employment_type_id: Optional[int] = Field(foreign_key="EmploymentTypes.id", default=None, index=True)
    location_id: Optional[int] = Field(foreign_key="Locations.id", index=True)
    status_id: int = Field(foreign_key="Statuses.id", index=True)

    company: "Company" = Relationship(back_populates="job_ads")
    education: "Education" = Relationship(back_populates="job_ads")
    location: Optional["Location"] = Relationship(back_populates="job_ads")
    employment_type: "EmploymentType" = Relationship(back_populates="job_ads")
    skills: List["Skill"] = Relationship(back_populates="job_ads", link_model=JobAdSkill)
    status: "Status" = Relationship(back_populates="job_ads")
    resumes: List["Resume"] = Relationship(back_populates="job_ads", link_model=Match)


class EmploymentType(SQLModel, table=True):
    __tablename__ = "EmploymentTypes"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(index=True, unique=True, nullable=False)

    job_ads: List["JobAd"] = Relationship(back_populates="employment_type")
    resumes: List["Resume"] = Relationship(back_populates="employment_type")


class Education(SQLModel, table=True):
    __tablename__ = "Education"

    id: int = Field(primary_key=True, index=True)
    degree_level: str = Field(index=True, unique=True, nullable=False)

    job_ads: List["JobAd"] = Relationship(back_populates="education")
    resumes: List["Resume"] = Relationship(back_populates="education")


class JobAdView(SQLModel, table=True):
    __tablename__ = "job_ads_view"
    id: int
    row_id: int = Field(primary_key=True)  # Surrogate primary key
    company_id: int
    title: str
    company_name: str
    description: Optional[str] = None
    degree_level: Optional[str] = None
    salary: Optional[float] = None
    Employment: Optional[str] = None
    Location: Optional[str] = None
    status: Optional[str] = None