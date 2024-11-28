from data.database import Session
from resumes.resume_services import get_all_resumes_with_skills_ids, get_resume_by_id, get_resume_with_ids_instead_of_names
from jobposts.jobpost_service import view_post_with_skills, view_post_with_strings_and_skills, view_posts_with_skills
import openai
from dotenv import load_dotenv
import os
from numpy import dot
from numpy.linalg import norm

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

openai.api_key = openai_key

def cosine_similarity(vec1, vec2):
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def get_embedding(text, model="text-embedding-ada-002"):
    # Make the API call to fetch embeddings
    response = openai.embeddings.create(
        model=model,
        input=text
    )
    # Correct way to access the embedding data
    embedding = response.data[0].embedding  # Access 'data' attribute and get 'embedding'
    return embedding

def titles_match(title1: str, title2: str, threshold=0.88) -> bool:
    embedding_1 = get_embedding(title1)
    embedding_2 = get_embedding(title2)
    similarity = cosine_similarity(embedding_1, embedding_2)
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
        return matching_ads
    
    
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
        return matching_resumes

    
    return None