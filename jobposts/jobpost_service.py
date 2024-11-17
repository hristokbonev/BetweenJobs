from fastapi import HTTPException
from sqlmodel import Session, select
from data.db_models import JobAd
from jobposts.jobpost_models import CreateJobAdRequest, UpdateJobAdRequest


def show_all_posts(session: Session):
    statement = select(JobAd)
    job_posts = session.execute(statement).scalars().all()

    return job_posts


def view_job_post_by_id(ad_id: int, session: Session):
    statement = select(JobAd).where(JobAd.id == ad_id)
    job_ad = session.execute(statement).scalars().first()
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
    target_job_ad = session.execute(statement).scalars().first()
    if not target_job_ad:
        raise HTTPException(status_code=404, detail="Job Ad not found.")

    # Get the data as a dictionary, excluding unset fields
    updates = data.dict(exclude_unset=True)

    # Dynamically update fields
    for field, value in updates.items():
        setattr(target_job_ad, field, value)

    session.commit()

    return target_job_ad
