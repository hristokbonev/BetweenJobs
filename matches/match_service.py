from fastapi import HTTPException
from sqlmodel import Session, select
from data.db_models import Resume, JobAd, ResumeSkill, Skill, JobAdSkill, User, Variables
from resumes import resume_services as rs
from jobposts import jobpost_service as js
from matches.match_models import MatchResponse
from common.mailjet_functions import send_email
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('all-mpnet-base-v2')


def titles_match(title1: str, title2: str, threshold=0.65) -> bool:
    embeddings = model.encode([title1, title2], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    return similarity >= threshold


def suggest_job_ads(resume_id, session: Session) -> list:
    resume = rs.get_resume_by_id(id=resume_id, session=session)

    if not resume:
        return None

    matching_ads = []

    for ad in js.show_posts_with_names_not_id(session):
        counter = 0
        counter_matches = 0

        if not titles_match(resume.title, ad.title):
            continue

        # Check if the resume education matches the ad education
        if resume.education and ad.education:
            counter += 1

            if resume.education == ad.education:
                counter_matches += 1

        # Check if the resume location matches the ad location

        if resume.location and ad.location:
            counter += 1

            if resume.location == ad.location:
                counter_matches += 1

        # Check if the resume skills match the ad skills

        if resume.skills and ad.skills:

            for skill in ad.skills:
                counter += 1
                if skill in resume.skills:
                    counter_matches += 1

        # Check if resume employment type matches the ad employment type

        if resume.employment_type and ad.employment:
            counter += 1

            if resume.employment_type == ad.employment:
                counter_matches += 1

        if counter_matches / counter >= 0.75:
            matching_ads.append(ad)

    if matching_ads:
        return matching_ads, resume

    return None


def match_with_job_ad(resume_id: int, job_ad_id: int, session: Session):
    # Fetch Resume details with relevant skills
    resume_query = select(Resume).where(Resume.id == resume_id)
    resume_skills_query = (
        select(Skill.id)
        .join(ResumeSkill, ResumeSkill.skill_id==Skill.id)
        .join(Resume, Resume.id==ResumeSkill.resume_id)
        .where(Resume.id == resume_id))

    resume = session.exec(resume_query).first()
    resume_skills = session.exec(resume_skills_query).all()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Fetch the user linked to the Resume
    user_query = select(User).where(User.id == resume.user_id)
    user = session.exec(user_query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found for the resume")

    # Fetch JobAd details with relevant skills
    job_ad_query = select(JobAd).where(JobAd.id == job_ad_id)
    job_ad_skills_query = (
        select(Skill.id)
        .join(JobAdSkill, JobAdSkill.skill_id == Skill.id)
        .join(JobAd, JobAd.id == JobAdSkill.jobad_id)
        .where(JobAd.id == job_ad_id)
    )

    job_ad = session.exec(job_ad_query).first()
    job_ad_skills = session.exec(job_ad_skills_query).all()
    if not job_ad:
        raise HTTPException(status_code=404, detail="JobAd not found")
    # Calculate match score by comparing location / education / employment type +1 point for each
    # Compare all skills in Resume and get +1 point for each match with JobAd skill
    match_score = 0
    top_score = len(job_ad_skills) + 3
    if resume.location_id == job_ad.location_id:
        match_score += 1
    if resume.education_id == job_ad.education_id:
        match_score += 1
    if resume.employment_type_id == job_ad.employment_type_id:
        match_score +=1

    for skill in resume_skills:
        if skill in job_ad_skills:
            match_score += 1
    # Update Resume status and Job Post status == Match
    match_score = round(match_score / top_score, 2)
    resume.status_id = 4
    job_ad.status_id = 4
    session.add(resume)
    session.add(job_ad)
    session.commit()

    statement = select(Variables)
    status = session.exec(statement).first()


    sender_email = 'fakeiei@yahoo.com' if status.email_test_mode else resume.full_name

    # Send email notification to jobseeker
    send_email(email='fakeiei@yahoo.com', name=(resume.full_name),
               text=f"Your match score for the possition of {job_ad.title} is {match_score/100}%",
               subject=f"BetweenJobs Match notification {job_ad.title}",
               html=f"<h1>Hello {resume.full_name}</h1>,\n\n"
                f"<h2>We have found a potential job match for you:</h2>\n"
                f"<p>Job Title: {job_ad.title}</p>\n"
                f"<p>Company: {job_ad.company_name}</p>\n"
                f"<p>Match Score: {match_score}%</p>\n\n"
                f"<p>Please log in to your account for more details.</p>\n\n"
                f"<h3>Best regards,</h3>\n"
                f"<h3>Your Job Portal Team</h3>"
               )
    # Send email notification to business owner

    return MatchResponse(
        user_id=resume.user_id,
        user_full_name=resume.full_name,
        user_profession=resume.title,
        job_position=job_ad.title,
        company_id=job_ad.company_id,
        company_name=job_ad.company_name,
        match_score=match_score
    )