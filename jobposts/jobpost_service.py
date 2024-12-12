from fastapi import HTTPException
from sqlmodel import Session, select
from typing import Any
from data.db_models import JobAd, Education, Location, EmploymentType, JobAdView, Status, JobAdSkill, Skill
from jobposts.jobpost_models import CreateJobAdRequest, JobAdResponseWithSkills, UpdateJobAdRequest, JobAddResponse, JobAdResponseWithNamesNotId
from sqlalchemy import Text, cast, func


def show_all_posts(session: Session, **filters: Any):
    statement = select(JobAd)
    for field, value in filters.items():
        if not value:
            continue

        if field == "location.name":
            statement = statement.join(JobAd.location).where(Location.name.ilike(f"%{value}%"))
        elif field == "employment.name":
            statement = statement.where(JobAd.employment_type).where(EmploymentType.name.ilike(f"%{value}%"))
        elif field == "region":
            statement = statement.where(JobAd.region.ilike(f"%{value}%"))
        else:
            column = getattr(JobAd, field, None)
            if column is not None:
                statement = statement.where(column.ilike(f"%{value}%"))

            
    job_posts = session.exec(statement).all()

    return job_posts


def view_job_post_by_id(ad_id: int, session: Session):
    statement = select(JobAd).where(JobAd.id == ad_id)
    job_ad = session.exec(statement).first()
    return job_ad


def create_job_post(data: CreateJobAdRequest, session: Session):
    # Add new job ad item
    new_post = JobAd(**data.model_dump())
    session.add(new_post)
    session.commit()

    response = view_job_post_by_id(new_post.id, session)
    return response


def change_job_post(target_id: int, data: UpdateJobAdRequest, session: Session):
    statement = select(JobAd).where(JobAd.id == target_id)
    target_job_ad = session.exec(statement).first()
    if not target_job_ad:
        raise HTTPException(status_code=404, detail="Job Ad not found.")

    # Get the data as a dictionary, excluding unset fields
    updates = data.dict(exclude_unset=True)

    # Dynamically update fields
    for field, value in updates.items():
        setattr(target_job_ad, field, value)

    session.commit()

    return target_job_ad


def view_jobs_by_company_id(comp_id: int, session: Session):
    statement = select(JobAdView).where(JobAdView.company_id == comp_id)
    job_ads = session.exec(statement).all()

    return [JobAddResponse(
        title=row.title,
        company_name=row.company_name,
        company_description=row.description,
        education=row.degree_level,
        salary=row.salary,
        employment=row.Employment,
        location=row.Location,
        status=row.status
    ) for row in job_ads]


def show_posts_with_names_not_id(session: Session):
   statement = (
        select(
            JobAd,
            Education.degree_level,
            Location.name,
            EmploymentType.name,
            Status.name,
            func.string_agg(Skill.name, ', ')
        ).join(Education, JobAd.education_id == Education.id, isouter=True).join
        (Location, JobAd.location_id == Location.id, isouter=True).join
        (EmploymentType, JobAd.employment_type_id == EmploymentType.id, isouter=True).join
        (Status, JobAd.status_id == Status.id, isouter=True).join
        (JobAdSkill, JobAd.id == JobAdSkill.jobad_id, isouter=True).join
        (Skill, JobAdSkill.skill_id == Skill.id, isouter=True).group_by(
            JobAd.id,  # Include all JobAd columns
            JobAd.created_at,
            JobAd.title,
            JobAd.company_name,
            JobAd.description,
            JobAd.salary,
            Education.degree_level,
            Location.name,
            EmploymentType.name,
            Status.name))
   
   job_posts = session.exec(statement).all()
   job_posts = [JobAdResponseWithNamesNotId(
    title=row[0].title,
    created_at=row[0].created_at,
    company_name=row[0].company_name,
    description=row[0].description,
    education=row[1],
    salary=row[0].salary,
    employment=row[3],
    location=row[2],
    status=row[4],
    id=row[0].id,
    skills=row[5].split(', ') if row[5] else []
    ) for row in job_posts]
   
   return job_posts

def view_posts_with_skills(session: Session):
    statement = (
        select(
            JobAd,
            func.string_agg(cast(Skill.id, Text), ', ')
        ).join(JobAdSkill, JobAd.id == JobAdSkill.jobad_id, isouter=True).join
        (Skill, JobAdSkill.skill_id == Skill.id, isouter=True).group_by(
            JobAd.id,  # Include all JobAd columns
            JobAd.created_at,
            JobAd.title,
            JobAd.company_name,
            JobAd.description,
            JobAd.salary,
            JobAd.education_id,
            JobAd.location_id,
            JobAd.employment_type_id,
            JobAd.status_id))
    
    job_posts = session.exec(statement).all()
    
    job_posts = [JobAdResponseWithSkills(
        id=row[0].id,
        title=row[0].title,
        created_at=row[0].created_at,
        company_name=row[0].company_name,
        description=row[0].description,
        education=row[0].education_id,
        salary=row[0].salary,
        employment=row[0].employment_type_id,
        location=row[0].location_id,
        status=row[0].status_id,
        skills=row[1].split(', ') if row[1] else []
    ) for row in job_posts]

    return job_posts


def view_post_with_strings_and_skills(ad_id: int, session: Session):
    
    statement = (
        select(
            JobAd,
            Education.degree_level,
            Location.name,
            EmploymentType.name,
            Status.name,
            func.string_agg(Skill.name, ', ')
        ).join(Education, JobAd.education_id == Education.id, isouter=True).join
        (Location, JobAd.location_id == Location.id, isouter=True).join
        (EmploymentType, JobAd.employment_type_id == EmploymentType.id, isouter=True).join
        (Status, JobAd.status_id == Status.id, isouter=True).join
        (JobAdSkill, JobAd.id == JobAdSkill.jobad_id, isouter=True).join
        (Skill, JobAdSkill.skill_id == Skill.id, isouter=True).group_by(
            JobAd.id,  # Include all JobAd columns
            JobAd.created_at,
            JobAd.title,
            JobAd.company_name,
            JobAd.description,
            JobAd.salary,
            Education.degree_level,
            Location.name,
            EmploymentType.name,
            Status.name)).where(JobAd.id == ad_id)
    
    job_post = session.exec(statement).first()
    
    if not job_post:
        return None
    
    job_post = JobAdResponseWithNamesNotId(
        title=job_post[0].title,
        created_at=job_post[0].created_at,
        company_name=job_post[0].company_name,
        description=job_post[0].description,
        education=job_post[1],
        salary=job_post[0].salary,
        employment=job_post[3],
        location=job_post[2],
        status=job_post[4],
        id=job_post[0].id,
        skills=job_post[5].split(', ') if job_post[5] else []
    )
    
    return job_post


def view_post_with_skills(ad_id: int, session: Session):
    statement = (
        select(
            JobAd,
            func.string_agg(cast(Skill.id, Text), ', ')
        ).join(JobAdSkill, JobAd.id == JobAdSkill.jobad_id, isouter=True).join
        (Skill, JobAdSkill.skill_id == Skill.id, isouter=True).group_by(
            JobAd.id,  # Include all JobAd columns
            JobAd.created_at,
            JobAd.title,
            JobAd.company_name,
            JobAd.description,
            JobAd.salary,
            JobAd.education_id,
            JobAd.location_id,
            JobAd.employment_type_id,
            JobAd.status_id)).where(JobAd.id == ad_id)
    
    job_post = session.exec(statement).first()
    
    if not job_post:
        return None
    
    job_post = JobAdResponseWithSkills(
        id=job_post[0].id,
        title=job_post[0].title,
        created_at=job_post[0].created_at,
        company_name=job_post[0].company_name,
        description=job_post[0].description,
        education=job_post[0].education_id,
        salary=job_post[0].salary,
        employment=job_post[0].employment_type_id,
        location=job_post[0].location_id,
        status=job_post[0].status_id,
        skills=job_post[1].split(', ') if job_post[1] else []
    )
    
    return job_post



def view_jobs_by_company_id_with_strings(comp_id: int, session: Session):
    statement = (
        select(
            JobAd,
            Education.degree_level,
            Location.name,
            EmploymentType.name,
            Status.name,
            func.string_agg(Skill.name, ', ')
        ).join(Education, JobAd.education_id == Education.id, isouter=True).join
        (Location, JobAd.location_id == Location.id, isouter=True).join
        (EmploymentType, JobAd.employment_type_id == EmploymentType.id, isouter=True).join
        (Status, JobAd.status_id == Status.id, isouter=True).join
        (JobAdSkill, JobAd.id == JobAdSkill.jobad_id, isouter=True).join
        (Skill, JobAdSkill.skill_id == Skill.id, isouter=True).group_by(
            JobAd.id,  # Include all JobAd columns
            JobAd.created_at,
            JobAd.title,
            JobAd.company_name,
            JobAd.description,
            JobAd.salary,
            Education.degree_level,
            Location.name,
            EmploymentType.name,
            Status.name)).where(JobAd.company_id == comp_id)
    
    job_ads = session.exec(statement).all()
    
    job_ads = [JobAdResponseWithNamesNotId(
        title=row[0].title,
        created_at=row[0].created_at,
        company_name=row[0].company_name,
        description=row[0].description,
        education=row[1],
        salary=row[0].salary,
        employment=row[3],
        location=row[2],
        status=row[4],
        id=row[0].id,
        skills=row[5].split(', ') if row[5] else []
    ) for row in job_ads]
    
    return job_ads


def view_jobs_by_company_id_with_id_included(session: Session, comp_id: int):
    statement = select(JobAd).where(JobAd.company_id == comp_id)
    job_ads = session.exec(statement).all()
    return job_ads