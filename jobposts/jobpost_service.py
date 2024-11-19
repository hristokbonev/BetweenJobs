from fastapi import HTTPException
from sqlmodel import Session, select
from data.db_models import JobAd, JobAdView
from jobposts.jobpost_models import CreateJobAdRequest, UpdateJobAdRequest, JobAddResponse


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
    statement = select(JobAdView).where(JobAdView.id == ad_id)
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
        status_name=row.status
    ) for row in job_ads]


def delete_job_ad(job_id: int, session: Session):
    statement = select(JobAd).where(JobAd.id == job_id)
    target_job_ad = session.exec(statement).first()
    if not target_job_ad:
        return None

    session.delete(target_job_ad)
    session.commit()

    return {"message": f"Job Posting with ID {job_id} and all related data was deleted!"}