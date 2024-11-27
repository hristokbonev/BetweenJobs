from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from companies.company_models import JobAddResponse
from jobposts.jobpost_models import CreateJobAdRequest, UpdateJobAdRequest
from data.database import get_session
from jobposts import jobpost_service as js
from resumes.resume_models import ResumeResponse
from users.user_models import UserModel
from utils import attribute_service as ats
from matches import match_services as ms
from utils.auth import get_current_user


job_post_router = APIRouter(prefix='/api/jobad', tags=["JobAds"])

@job_post_router.get('/{job_id}', response_model=JobAddResponse)
def show_job_ad_by_id(job_id: int, session: Session = Depends(get_session)):
    try:
        job_ad = js.view_job_post_by_id(ad_id=job_id, session=session)
        if not job_ad:
            raise HTTPException(status_code=404, detail=f"Job Ad with ID {job_id} not found.")
        education = ats.view_education_by_id(job_ad.education_id, session)
        employment = ats.get_employment_by_id(job_ad.employment_type_id, session)
        location = ats.get_location_by_id(job_ad.location_id, session)

        return JobAddResponse(
            title=job_ad.title,
            company_name=job_ad.company_name,
            company_description=job_ad.description,
            education=education,
            salary=job_ad.salary,
            employment=employment,
            location=location
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@job_post_router.post('/', response_model=JobAddResponse)
def register_new_job_ad(data: CreateJobAdRequest, session: Session = Depends(get_session)):
    try:
        new_job_ad = js.create_job_post(data=data, session=session)
        if not new_job_ad:
            raise HTTPException(status_code=500, detail=f"Failed to create job ad with name {data.title}.")

        new_job = show_job_ad_by_id(job_id=new_job_ad.id, session=session)

        return JobAddResponse(**dict(new_job))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@job_post_router.put('/{job_id}', response_model=JobAddResponse)
def modify_jobad_by_id(job_id: int, data: UpdateJobAdRequest, session: Session = Depends(get_session)):
    try:
        updated_job_ad = js.change_job_post(job_id, data, session)
        return updated_job_ad
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Server error: {str(e)}')


@job_post_router.get('/', response_model=None)

def suggest_resumes(job_id: int, session: Session = Depends(get_session), current_user: UserModel = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="You must be logged in to view resumes")
    try:
        a = (datetime.now())
        resumes = ms.suggest_resumes(job_id, session)
        b = (datetime.now())
        print(b-a)
        return resumes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
