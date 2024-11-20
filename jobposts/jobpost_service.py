from fastapi import HTTPException
from sqlmodel import Session, select, delete
from data.db_models import JobAd, JobAdView, Skill, JobAdSkill
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
    new_job_post = JobAd(**data.model_dump())
    session.add(new_job_post)
    # Save changes with new job ID
    session.flush()
    # Assign all skills related to the JobAd
    if data.skill_ids:
        for skill_id in data.skill_ids:
            statement = select(Skill.id).where(Skill.id == skill_id)
            session.exec(statement).first()
            job_ad_skill = JobAdSkill(jobad_id=new_job_post.id, skill_id=skill_id)
            session.add(job_ad_skill)

    session.commit()

    response = view_job_post_by_id(new_job_post.id, session)
    return response


def change_job_post(target_id: int, data: UpdateJobAdRequest, session: Session):
    # Fetch the target JobAd record
    statement = select(JobAd).where(JobAd.id == target_id)
    target_job_post = session.exec(statement).first()
    if not target_job_post:
        raise HTTPException(status_code=404, detail="Job Ad not found.")

    # Update all items in JobAd, excluding the list of skill ids
    updates = data.dict(exclude_unset=True, exclude={"skill_ids"})

    for field, value in updates.items():
        setattr(target_job_post, field, value)

    session.flush()
    # Update skills in the JobAdSkill table if skill_ids are provided
    if data.skill_ids is not None:
        current_skills = session.exec(
            select(JobAdSkill.skill_id).where(JobAdSkill.jobad_id == target_id)
        ).all()
        current_skill_ids = set(current_skills)
        new_skill_ids = set(data.skill_ids)

        # Calculate skills to add and remove
        skills_to_add = new_skill_ids - current_skill_ids
        skills_to_remove = current_skill_ids - new_skill_ids

        # Add new skills
        for skill_id in skills_to_add:
            skill_exists = session.exec(select(Skill).where(Skill.id == skill_id)).first()
            if not skill_exists:
                raise HTTPException(status_code=400, detail=f"Skill ID {skill_id} does not exist.")
            new_skill = JobAdSkill(jobad_id=target_id, skill_id=skill_id)
            session.add(new_skill)

        # Remove outdated skills
        if skills_to_remove:
            session.exec(
                delete(JobAdSkill).where(
                    JobAdSkill.jobad_id == target_id, JobAdSkill.skill_id.in_(skills_to_remove)
                )
            )
        # Commit changes to the database
    session.commit()

    response = view_job_post_by_id(target_id, session)
    return response



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