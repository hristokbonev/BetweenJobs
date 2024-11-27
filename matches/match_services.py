from data.database import Session
from resumes.resume_services import get_all_resumes_with_skills_ids, get_resume_by_id, get_resume_with_ids_instead_of_names
from jobposts.jobpost_service import view_post_with_skills, view_post_with_strings_and_skills, view_posts_with_skills
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('all-MiniLM-L6-v2')


def titles_match(title1: str, title2: str, threshold=0.65) -> bool:
    embeddings = model.encode([title1, title2], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    return similarity >= threshold


def suggest_job_ads(resume_id, session: Session) -> list:

    resume = get_resume_with_ids_instead_of_names(id=resume_id, session=session)

    if not resume:
        return None

    matching_ads = []

    for ad in view_posts_with_skills(session):
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
        

        if counter_matches/counter >= 0.75:
            ad = view_post_with_strings_and_skills(ad.id, session)
            matching_ads.append(ad)

    if matching_ads:
        return matching_ads, resume
    
    
    return None



def suggest_resumes(ad_id: int, session: Session) -> list:

    ad = view_post_with_skills(ad_id, session)

    if not ad:
        return None
    
    matching_resumes = []

    for resume in get_all_resumes_with_skills_ids(session):
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
        

        if counter_matches/counter >= 0.75:
            resume = get_resume_by_id(resume.id, session)
            matching_resumes.append(resume)

    if matching_resumes:
        return matching_resumes, ad

    
    return None