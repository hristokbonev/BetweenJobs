from typing import Optional

from sqlmodel import Session, select
from data.db_models import Education, EmploymentType, Location, Skill, Status, JobAdSkill, SkillLevel, ResumeSkill


def view_education_by_id(education_id: int, session: Session):
    statement = select(Education.degree_level).where(Education.id == education_id)
    education = session.exec(statement).first()
    return education


def get_employment_by_id(employment_id: int, session: Session):
    statement = select(EmploymentType.name).where(EmploymentType.id == employment_id)
    employment = session.exec(statement).first()
    return employment


def get_location_by_id(location_id: int, session: Session):
    statement = select(Location.name).where(Location.id == location_id)
    location = session.exec(statement).first()
    return location

def get_status_by_id(status_id: int, session: Session):
    statement = select(Status.name).where(Status.id == status_id)
    status = session.exec(statement).first()

# Used to dynamically call column values for dynamic reference
# Used for Education, EmploymentType, Skills, Location
def get_distinct_column_values(session: Session, column):
    statement = select(column).distinct()
    results = session.exec(statement).all()
    return [value for value, in results if value]


def education_exists(education, session: Session):
    statement = select(Education.id).where(Education.degree_level == education)
    education_type = session.exec(statement).first()

    return bool(education_type)


def employment_type_exists(employment_type, session: Session):
    statement = select(EmploymentType.name).where(EmploymentType.name == employment_type)
    employment_type_name = session.exec(statement).first()
    return bool(employment_type_name)


def get_all_locations(session: Session):
    statement = select(Location.name)
    locations = session.exec(statement).all()
    return locations if locations else None


def location_exists(location, session: Session):
    statement = select(Location.name).where(Location.name == location)
    location = session.exec(statement).first()
    return bool(location)


def skill_exists(skill, session: Session):
    statement = select(Skill.name).where(Skill.name == skill)
    skill = session.exec(statement).first()
    return bool(skill)


def status_exists(status, session: Session):
    statement = select(Status.name).where(Status.name == status)
    status_type = session.exec(statement).first()
    return bool(status_type)


def assign_skills(company_id: int,
    post_id: int,
    target: str,
    skill_ids: list[int],
    skill_levels: Optional[list[int]],
    session: Session):
    '''Evaluates each skill in skill_ids and maps the skill id to the relevant JobAd or Resume
    use target=jobpost to assign skills to job ad or target =resume to assing skills to resume'''

    if target == 'jobpost':
        for idx, skill_id in enumerate(skill_ids):
            job_skill = JobAdSkill(jobad_id=post_id, skill_id=skill_id)
            session.add(job_skill)

            # Check and assign skill levels or use default level if none is provided
            skill = session.get(Skill, skill_id)
            if skill and skill.is_scalable:
                level_id = skill_levels[idx] if skill_levels and idx < len(skill_levels) else 1

                skill = SkillLevel(skill_id=skill_id, level_id=level_id)
                session.add(skill)

    elif target == 'resume':
        for idx, skill_id in enumerate(skill_ids):
            job_skill = ResumeSkill(resume_id=post_id, skill_id=skill_id)
            session.add(job_skill)

            # Check and assign skill levels or use default level if none is provided
            skill = session.get(Skill, skill_id)
            if skill and skill.is_scalable:
                level_id = skill_levels[idx] if skill_levels and idx < len(skill_levels) else 1

                skill = SkillLevel(skill_id=skill_id, level_id=level_id)
                session.add(skill)