from sqlmodel import Session, select
from data.db_models import Company, Resume, User, Variables, ResumeMatchJobAd, JobAd, JobAdMatchResume
from users.user_models import UserSearch, UserUpdate, UserModel, TestModeResponse, UserCreate
from data.db_models import Skill
from users.user_models import CreateSkillRequest
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jobposts.jobpost_service import view_post_with_strings_and_skills

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/users/login', auto_error=False)

def get_password_hash(password: str):
    return pwd_context.hash(password)

# redundant
def view_users(session: Session):
    statement = select(User).order_by(User.id)
    users = session.exec(statement).all()

    return users


def view_user_by_id(user_id: int, session: Session):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    return user


# ADMIN Functions
def create_new_skill(data: CreateSkillRequest, session: Session):
    # Check if skill exists
    is_skill = select(Skill).where(Skill.name == data.name)
    existing_skill = session.execute(is_skill).scalars().first()
    if existing_skill:
        raise ValueError(f'Skill {data.skill_name} already exists!')
    # Create new skill record
    new_skill = Skill(**data.model_dump())
    session.add(new_skill)
    session.commit()
    # Return the newly created skill
    find_new_skill = select(Skill).where(Skill.id == new_skill.id)
    response = session.execute(find_new_skill).scalars().first()
    return response


def get_filtered_users(search_criteria: UserSearch, page: int, limit: int, session: Session):
    statement = select(User)
    if search_criteria.username:
        statement = statement.filter(User.username.ilike(f"%{search_criteria.username}%"))
    if search_criteria.first_name:
        statement = statement.filter(User.first_name.ilike(f"%{search_criteria.first_name}%"))
    if search_criteria.last_name:
        statement = statement.filter(User.last_name.ilike(f"%{search_criteria.last_name}%"))
    if search_criteria.email:
        statement = statement.filter(User.email.ilike(f"%{search_criteria.email}%"))

    offset = (page - 1) * limit
    statement = statement.offset(offset).limit(limit)
    users = session.exec(statement).all()
    return users


def update_user(user_id: int, user_update, session: Session):
    stm = select(User).where(User.id == user_id)
    user = session.exec(stm).first()
    
    if not user:
        return None
    
    user.username = user_update.username or user.username

    if user_update.new_password or user_update.confirm_password:
        if user_update.new_password != user_update.confirm_password:
            raise ValueError("New password and confirm password do not match")
        user.password = get_password_hash(user_update.new_password)

    user.first_name = user_update.first_name or user.first_name
    user.last_name = user_update.last_name or user.last_name
    user.email = user_update.email or user.email

  
    session.add(user)
    session.commit()
    session.refresh(user)
  
    return user


def swith_test_mode(session: Session, user: UserModel):
    statement = select(Variables).where(Variables.var_id==1)
    status = session.exec(statement).first()
    if status.email_test_mode:
        status.email_test_mode = 0
    else:
        status.email_test_mode = 1

    session.add(status)
    session.commit()
    session.refresh(status)

    return TestModeResponse(status=status.email_test_mode)


def get_user(username: str, user_id: str, session: Session) -> UserCreate:
    statement = select(User).where(User.username == username, User.id == user_id)
    user = session.exec(statement).first()
    if not user:
        return None
    return UserModel(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_admin=user.is_admin,
        date_of_birth=user.date_of_birth,
    )


def user_has_companies(user_id: int, session: Session) -> bool:
    statement = select(User).where(User.id == user_id).join(Company, Company.author_id == User.id).limit(1)
    user = session.exec(statement).first()
    return bool(user)


def rejected_jobs(user_id: int, session: Session):
    statement = select(JobAd).join(ResumeMatchJobAd, ResumeMatchJobAd.jobad_id == JobAd.id)\
    .join(Resume, ResumeMatchJobAd.resume_id == Resume.id)\
    .join(User, Resume.user_id == User.id)\
    .where(User.id == user_id, ResumeMatchJobAd.accepted == False)

    jobs = session.exec(statement).all()
    jobs = [view_post_with_strings_and_skills(job.id, session) for job in jobs]
    return jobs


def accepted_jobs(user_id: int, session: Session):
    statement = select(JobAd).join(ResumeMatchJobAd, ResumeMatchJobAd.jobad_id == JobAd.id)\
    .join(Resume, ResumeMatchJobAd.resume_id == Resume.id)\
    .join(User, Resume.user_id == User.id).where(User.id == user_id, ResumeMatchJobAd.accepted == True)
    jobs = session.exec(statement).all()
    jobs = [view_post_with_strings_and_skills(job.id, session) for job in jobs]
    return jobs


def owns_job_ad(user_id: int, job_ad_id: int, session: Session) -> bool:
    statement = select(JobAd).join(Company, Company.id == JobAd.company_id).where(JobAd.id == job_ad_id, Company.author_id == user_id).limit(1)
    job = session.exec(statement).first()
    return bool(job)


def accepted_resumes(user_id: int, session: Session):
    statement = select(Resume).join(JobAdMatchResume, JobAdMatchResume.resume_id == Resume.id)\
    .join(JobAd, JobAdMatchResume.jobad_id == JobAd.id).join(Company, Company.id == JobAd.company_id)\
    .where(Company.author_id == user_id, JobAdMatchResume.accepted == True)

    resumes = session.exec(statement).all()
    return resumes
    

def rejected_resumes(user_id: int, session: Session):
    statement = select(Resume).join(JobAdMatchResume, JobAdMatchResume.resume_id == Resume.id)\
    .join(JobAd, JobAdMatchResume.jobad_id == JobAd.id).join(Company, Company.id == JobAd.company_id)\
    .where(Company.author_id == user_id, JobAdMatchResume.accepted == False)

    resumes = session.exec(statement).all()
    return resumes