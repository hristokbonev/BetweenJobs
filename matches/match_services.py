from data.database import Session
import re
from resumes.resume_services import get_resume_by_id
from jobposts.jobpost_service import show_posts_with_names_not_id



def suggest_job_ads(resume_id, session: Session) -> list:

    resume = get_resume_by_id(id=resume_id, session=session)

    if not resume:
        return None

    matching_ads = []

    for ad in show_posts_with_names_not_id(session):
        counter = 0
        counter_matches = 0

    # Check if the resume title and the ad title have any common words
        resume_title = set(resume.title.lower().split())
        ad_title = set(ad.title.lower().split())

        if not resume_title & ad_title:
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
        

        if counter_matches/counter >= 0.75:
            matching_ads.append(ad)

    if matching_ads:
        return matching_ads, resume
    
    return None