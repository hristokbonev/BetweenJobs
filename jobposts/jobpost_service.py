from fastapi import HTTPException
from sqlmodel import Session, select
from data.db_models import JobAd, Education, Location, EmploymentType, JobAdView, Status, JobAdSkill, Skill
from jobposts.jobpost_models import CreateJobAdRequest, UpdateJobAdRequest, JobAddResponse, JobAdResponseWithNamesNotId
from sqlalchemy import func
from utils import attribute_service as ats


def show_all_posts(
            session: Session,
            page: int,
            limit: int,
            title: str,
            company_name: str,
            location: str,
            employment_type: str,
            education: str,
            status: str
    ):
        filters = []
        if title:
            filters.append(JobAdView.title == title)
        if company_name:
            filters.append(JobAdView.company_name == company_name)
        if location:
            filters.append(JobAdView.Location == location)
        if employment_type:
            filters.append(JobAdView.Employment == employment_type)
        if education:
            filters.append(JobAdView.degree_level == education)
        if status:
            filters.append(JobAdView.status == status)

        # Build the statement with all filters
        offset = (page - 1) * limit
        statement = select(JobAdView).where(*filters).offset(offset).limit(limit)
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


def view_job_post_by_id(ad_id: int, session: Session):
    statement = select(JobAd).where(JobAd.id == ad_id)
    job_ad = session.exec(statement).first()
    education = session.exec(select(Education.degree_level).where(Education.id == job_ad.education_id)).first()
    location = ats.get_location_by_id(job_ad.location_id, session)
    employment = ats.get_employment_by_id(job_ad.employment_type_id, session)
    status = ats.view_education_by_id(job_ad.status_id, session)
    return JobAddResponse(
        title=job_ad.title,
        company_name=job_ad.company_name,
        company_description=job_ad.description,
        education=education,
        salary=job_ad.salary,
        employment=employment,
        location=location,
        status=status
        )

def create_job_post(data: CreateJobAdRequest, session: Session):
    # Add new job ad item
    new_post = JobAd(**data.model_dump())
    session.add(new_post)
    session.commit()

    # Check if list of skills is provided
    if data.skill_ids:
        ats.assign_skills(
            company_id=data.company_id,
            post_id=new_post.id,
            target='jobpost',
            skill_ids=data.skill_ids,
            skill_levels=data.skill_levels,
            session=session
        )
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
        location=row.Location
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
    skills=row[5].split(', ') if row[5] else []
    ) for row in job_posts]
   
   return job_posts