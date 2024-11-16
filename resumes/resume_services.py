from data.database import get_session
from fastapi import Depends
from data.db_models import Resume, EmploymentType, Education, Status, User, Location
from sqlmodel import select, Session
from resumes.resume_models import ResumeResponse

def get_all_resumes(session: Session):

    statement = (select(Resume.id, Resume.user_id, Resume.full_name, Resume.title, Resume.job_description,
                        User.username, EmploymentType.name, Education.degree_level, Location.name, Status.name).join
                        (User, User.id == Resume.user_id).join
                        (EmploymentType,EmploymentType.id == Resume.employment_type_id).join
                        (Education, Education.id == Resume.education_id).join(Status, Status.id == Resume.status_id).join
                        (Location, Location.id == Resume.location_id, isouter=True))

    resumes = session.execute(statement).all()


    return [ResumeResponse(
            id=tpl[0],
            user_id=tpl[1],
            full_name=tpl[2],
            title=tpl[3],
            job_description=tpl[4],
            username=tpl[5],
            employment_type=tpl[6],
            education=tpl[7],
            location=tpl[8],
            status=tpl[9]
        ) for tpl in resumes] if resumes else None


def get_resume_by_id(id, session: Session):

    statement = (select(Resume.id, Resume.user_id, Resume.full_name, Resume.title, Resume.job_description,
                        User.username, EmploymentType.name, Education.degree_level, Location.name, Status.name).join
                        (User, User.id == Resume.user_id).join
                        (EmploymentType,EmploymentType.id == Resume.employment_type_id).join
                        (Education, Education.id == Resume.education_id, isouter=True).join(Status, Status.id == Resume.status_id).join
                        (Location, Location.id == Resume.location_id, isouter=True)).where(Resume.id == id)


    resume = session.execute(statement).first()

    resume = ResumeResponse(id=resume[0], user_id=resume[1], full_name=resume[2], title=resume[3], job_description=resume[4],
                            username=resume[5], employment_type=resume[6], education=resume[7], location=resume[8], status=resume[9])
    
    return resume if resume else None