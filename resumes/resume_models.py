from typing import Literal
from pydantic import BaseModel
from pydantic import field_validator
from utils.attribute_service import education_exists, location_exists, employment_type_exists, skill_exists, status_exists
from data.database import engine, Session


class ResumeResponse(BaseModel):

    user_id: int
    username: str
    full_name: str | None = None
    title: str
    education: str | None = None
    summary: str | None = None
    status: str
    employment_type: str | None = None
    location: str | None = None
    id: int
    skills: list[str] | None = None
    salary: int | None = None

    class Config:
        from_attributes = True


class ResumeResponseWithIds(BaseModel):

    id: int | None = None
    user_id: int
    full_name: str | None = None
    title: str
    education: int | None = None
    summary: str | None = None
    status: int
    employment_type: int | None = None
    location: int | None = None
    skills: list[int] | None = None
    salary: int | None = None

    class Config:
        from_attributes = True


class ResumeRequest(BaseModel):

    full_name: str | None = None
    title: str 
    education: Literal['High school', 'Diploma', 'Undergraduate degree', 'Postgraduate degree', 'PhD'] | None = None
    summary: str | None = None
    status: Literal['Active', 'Hidden', 'Private', 'Matched', 'Archived', 'Busy'] = 'Active'
    employment_type: Literal['Full-time', 'Part-time', 'Temporary', 'Zero-hour contract', 'Casual employment', 'Internship'] | None = None
    location: str | None = None
    skills: list[str] | None = None
    salary: int | None = None

    @field_validator('education')
    @classmethod
    def validate_education(cls, value):
        if value:
            with Session(engine) as session:
                if not education_exists(value, session):
                    raise ValueError(f"Education {value} does not exist")
        return value.capitalize()
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, value):
        if value:
            with Session(engine) as session:
                if not status_exists(value, session):
                    raise ValueError(f"Status {value} does not exist")
        return value
    
    @field_validator('employment_type')
    @classmethod
    def validate_employment_type(cls, value):
        if value:
            with Session(engine) as session:
                if not employment_type_exists(value, session):
                    raise ValueError(f"Employment type {value} does not exist")
        return value
    

    @field_validator('location')
    @classmethod
    def validate_location(cls, value):
        if value:
            with Session(engine) as session:
                if not location_exists(value, session):
                    raise ValueError(f"Location {value} does not exist")
        return value
    
    @field_validator('skills')
    @classmethod
    def validate_skills(cls, value):
        if value:
            with Session(engine) as session:
                for skill in value:
                    if not skill_exists(skill, session):
                        raise ValueError(f"Skill {skill} does not exist")         
        return value
    
    @field_validator('salary')
    @classmethod
    def validate_salary(cls, value):
        if value:
            if value < 0:
                raise ValueError("Salary cannot be negative")
        return value

    class Config:
        from_attributes = True


class ResumeUpdate(BaseModel):
    
        full_name: str | None = None
        title: str | None = None
        education: str | None = None
        summary: str | None = None
        status: str | None = None
        employment_type: str | None = None
        location: str | None = None
        skills: list[str] | None = None
        salary: int | None = None
    
        @field_validator('education')
        @classmethod
        def validate_education(cls, value):
            if value:
                with Session(engine) as session:
                    if not education_exists(value, session):
                        raise ValueError(f"Education {value} does not exist")
            return value
        
        @field_validator('status')
        @classmethod
        def validate_status(cls, value):
            if value:
                with Session(engine) as session:
                    if not status_exists(value, session):
                        raise ValueError(f"Status {value} does not exist")
            return value
        
        @field_validator('employment_type')
        @classmethod
        def validate_employment_type(cls, value):
            if value:
                with Session(engine) as session:
                    if not employment_type_exists(value, session):
                        raise ValueError(f"Employment type {value} does not exist")
            return value
    
        @field_validator('location')
        @classmethod
        def validate_location(cls, value):
            if value:
                with Session(engine) as session:
                    if not location_exists(value, session):
                        raise ValueError(f"Location {value} does not exist")
            return value
        
        @field_validator('skills')
        @classmethod
        def validate_skills(cls, value):
            if value:
                with Session(engine) as session:
                    for skill in value:
                        if not skill_exists(skill, session):
                            raise ValueError(f"Skill {skill} does not exist")
            return value
        
        @field_validator('salary')
        @classmethod
        def validate_salary(cls, value):
            if value:
                if value < 0:
                    raise ValueError("Salary cannot be negative")
            return value
    
        class Config:
            from_attributes = True