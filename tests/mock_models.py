from unittest.mock import MagicMock
from data.db_models import Resume, Location, Education, ResumeSkill, Status, EmploymentType, Skill
from resumes.resume_models import ResumeRequest, ResumeResponse, ResumeResponseWithIds


def mock_resume(id: int, full_name: str, title: str, education_id: int, summary: str, location_id: int, status_id: int, employment_type_id: int):

    resume = MagicMock(spec=Resume)
    resume.id = id
    resume.full_name = full_name
    resume.title = title
    resume.education_id = education_id
    resume.summary = summary
    resume.location_id = location_id
    resume.status_id = status_id
    resume.employment_type_id = employment_type_id

    return resume

def mock_resume_response(id: int, user_id: int, full_name: str, title: str, summary: str, username: str, employment_type: str, education: str, location: str, status: str, skills: list):

    resume = MagicMock(spec=ResumeResponse)
    resume.id = id
    resume.user_id = user_id
    resume.full_name = full_name
    resume.title = title
    resume.summary = summary
    resume.username = username
    resume.employment_type = employment_type
    resume.education = education
    resume.location = location
    resume.status = status
    resume.skills = skills
    
    return resume

def mock_resume_response_with_ids(id: int, user_id: int, full_name: str, title: str, summary: str, username: str, employment_type: int, education: int, location: int, status: int, skills: list):

    resume = MagicMock(spec=ResumeResponseWithIds)
    resume.id = id
    resume.user_id = user_id
    resume.full_name = full_name
    resume.title = title
    resume.summary = summary
    resume.username = username
    resume.employment_type = employment_type
    resume.education = education
    resume.location = location
    resume.status = status
    resume.skills = skills
    
    return resume


def mock_resume_request(full_name: str = None, title: str = None, education: str | int = None, 
                        summary: str = None, status: str | int = None, employment_type: str | int = None, 
                        location: str | int = None, skills: list = None):
  
    resume = MagicMock(spec=ResumeRequest)
    resume.full_name = full_name
    resume.title = title
    resume.education = education
    resume.summary = summary
    resume.status = status
    resume.employment_type = employment_type
    resume.location = location
    resume.skills = skills

    return resume

def mock_location(name: str, id: int):

    location = MagicMock(spec=Location)
    location.name = name
    location.id = id

    return location

def mock_education(degree_level: str, id: int):
    
    education = MagicMock(spec=Education)
    education.degree_level = degree_level
    education.id = id

    return education

def mock_status(name: str, id: int):
     
    status = MagicMock(spec=Status)
    status.name = name
    status.id = id

    return status

def mock_employment_type(name: str, id: int):
    
    employment_type = MagicMock(spec=EmploymentType)
    employment_type.name = name
    employment_type.id = id

    return employment_type

def mock_skill(name: str, id: int):
        
    skill = MagicMock(spec=Skill)
    skill.name = name
    skill.id = id

    skill.resumes = []
    skill.job_ads = []
    skill.levels = []
    
    return skill

def mock_resume_skill(resume_id: int, skill_id: int):
    
    resume_skill = MagicMock(spec=ResumeSkill)
    resume_skill.resume_id = resume_id
    resume_skill.skill_id = skill_id
    
    return resume_skill