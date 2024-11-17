from gotrue.helpers import model_dump
from sqlmodel import Session, select
from data.db_models import JobAd
from jobposts.jobpost_models import JobAdRequest


def show_all_posts(session: Session):
    statement = select(JobAd)
    job_posts = session.execute(statement).scalars().all()

    return job_posts


def create_job_post(data: JobAdRequest, session: Session):
    # Add new job ad item
    new_post = JobAd(**data.model_dump())
    session.add(new_post)
    session.commit()

    return None
