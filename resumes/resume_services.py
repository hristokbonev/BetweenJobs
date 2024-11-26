from sqlalchemy import func
from data.db_models import Resume, EmploymentType, Education, ResumeSkill, Status, User, Location, Skill
from sqlmodel import select, Session
from resumes.resume_models import ResumeResponse, ResumeResponseWithIds
from users.user_models import UserModel

def get_all_resumes(session: Session, name: str, location: str, employment_type: str, education: str, status: str, title: str, skills: list):

    statement = (
        select(
            Resume.id, Resume.user_id, Resume.full_name, Resume.title, Resume.summary,
            User.username, EmploymentType.name, Education.degree_level, Location.name, Status.name
            )
        .join(User, User.id == Resume.user_id)
        .join(EmploymentType, EmploymentType.id == Resume.employment_type_id)
        .join(Education, Education.id == Resume.education_id, isouter=True)
        .join(Status, Status.id == Resume.status_id)
        .join(Location, Location.id == Resume.location_id, isouter=True)
        )
   
    if name:
        statement = statement.where(Resume.full_name == name)

    if title:
        statement = statement.where(Resume.title.ilike(f"%{title}%"))

    if location:
        statement = statement.where(Location.name == location)

    if employment_type:
        statement = statement.where(EmploymentType.name == employment_type)

    if education:
        statement = statement.where(Education.degree_level == education)

    if status:
        statement = statement.where(Status.name == status)

    if skills:
        statement = statement.join(ResumeSkill, ResumeSkill.resume_id == Resume.id)
        statement = statement.join(Skill, Skill.id == ResumeSkill.skill_id)
        statement = statement.where(Skill.name.in_(skills))

    resumes = session.exec(statement).all()

    if not resumes:
        return None

    resumes_list = []

    for resume in resumes:
        resume = ResumeResponse(
            id=resume[0],
            user_id=resume[1],
            full_name=resume[2],
            title=resume[3],
            summary=resume[4],
            username=resume[5],
            employment_type=resume[6],
            education=resume[7],
            location=resume[8],
            status=resume[9])
        
        resume.skills = [session.exec(select(Skill.name).join(ResumeSkill, ResumeSkill.skill_id==Skill.id).join(Resume, Resume.id==ResumeSkill.resume_id).where(Resume.id == resume.id)).all()]
        
        resumes_list.append(resume)

    return resumes_list if resumes_list else None


def get_resume_by_id(id, session: Session):

    statement = (select(Resume.id, Resume.user_id, Resume.full_name, Resume.title, Resume.summary,
                        User.username, EmploymentType.name, Education.degree_level, Location.name, Status.name).join
                        (User, User.id == Resume.user_id).join
                        (EmploymentType,EmploymentType.id == Resume.employment_type_id, isouter=True).join
                        (Education, Education.id == Resume.education_id, isouter=True).join(Status, Status.id == Resume.status_id).join
                        (Location, Location.id == Resume.location_id, isouter=True).where(Resume.id == id)).limit(1)


    resume = session.exec(statement).first()

    if not resume:
        return None

    resume = ResumeResponse(id=resume[0], user_id=resume[1], full_name=resume[2], title=resume[3], summary=resume[4],
                            username=resume[5], employment_type=resume[6], education=resume[7], location=resume[8], status=resume[9])
    
    resume.skills = [session.exec(select(Skill.name).join(ResumeSkill, ResumeSkill.skill_id==Skill.id).join(Resume, Resume.id==ResumeSkill.resume_id).where(Resume.id == resume.id)).all()]

    
    return resume if resume else None

def create_resume(resume_form, session: Session, user: UserModel):

    location = resume_form.location
    if location:
        statement = select(Location.id).where(Location.name == resume_form.location)
        location = session.exec(statement).first()

    employment_type = resume_form.education
    if employment_type:
        statement = select(EmploymentType.id).where(EmploymentType.name == resume_form.employment_type)
        employment_type = session.exec(statement).first()

    statement = select(Status.id).where(Status.name == resume_form.status)
    status_id = session.exec(statement).first()

    education = resume_form.education
    if education:
        statement = select(Education.id).where(Education.degree_level == resume_form.education)
        education = session.exec(statement).first()

    resume = Resume(user_id=user.id.user_id,
                    full_name=resume_form.full_name, 
                    title=resume_form.title,
                    education_id=education,
                    summary=resume_form.summary,
                    location_id=location,
                    status_id=status_id,
                    employment_type_id=employment_type)
    
    
    session.add(resume)
    session.commit()

    new_id = resume.id

    if resume_form.skills:
        for skill in resume_form.skills:
            statement = select(Skill.id).where(Skill.name == skill)
            skill_id = session.exec(statement).first()
            resume_skill = ResumeSkill(resume_id=resume.id, skill_id=skill_id)
            session.add(resume_skill)

    session.commit()

    return get_resume_by_id(new_id, session)


def update_resume(id, resume_form, session: Session):

    statement = select(Resume).where(Resume.id == id)

    resume = session.exec(statement).first()

    if not resume:
        return None

    resume.full_name = resume_form.full_name if resume_form.full_name else resume.full_name
    resume.title = resume_form.title if resume_form.title else resume.title
    resume.summary = resume_form.summary if resume_form.summary else resume.summary
    if resume_form.education:
        statement = select(Education.id).where(Education.degree_level == resume_form.education)
        resume.education_id = session.exec(statement).first()
    if resume_form.location:
        statement = select(Location.id).where(Location.name == resume_form.location)
        resume.location_id = session.exec(statement).first()
    if resume_form.status:
        statement = select(Status.id).where(Status.name == resume_form.status)
        resume.status_id = session.exec(statement).first()     
    if resume_form.employment_type:
        statement = select(EmploymentType.id).where(EmploymentType.name == resume_form.employment_type)
        resume.employment_type_id = session.exec(statement).first()

    session.add(resume)
    session.commit()
    
    if resume_form.skills:
        for skill in resume_form.skills:
            statement = select(Skill.id).where(Skill.name == skill)
            skill_id = session.exec(statement).first()
            resume_skill = ResumeSkill(resume_id=resume.id, skill_id=skill_id)
            session.add(resume_skill)
    
    session.commit()

    return get_resume_by_id(resume.id, session)


def delete_resume(id, session: Session):
    
    statement = select(Resume).where(Resume.id == id)
    resume = session.exec(statement).first()

    if not resume:
        return None
    
    session.delete(resume)
    session.commit()

    return resume

def get_resume_with_ids_instead_of_names(id, session: Session):

    statement = select(Resume).where(Resume.id == id)

    resume = session.exec(statement).first()

    resume = ResumeResponseWithIds(id=resume.id, user_id=resume.user_id, full_name=resume.full_name, title=resume.title, summary=resume.summary,
                                   employment_type=resume.employment_type_id, education=resume.education_id, location=resume.location_id, status=resume.status_id)
    
    resume.skills = [session.exec(select(Skill.id).join(ResumeSkill, ResumeSkill.skill_id==Skill.id).join(Resume, Resume.id==ResumeSkill.resume_id).where(Resume.id == resume.id)).all()]

    return resume if resume else None



    