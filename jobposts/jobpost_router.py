from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from companies.company_models import JobAddResponse
from jobposts.jobpost_models import CreateJobAdRequest, UpdateJobAdRequest
from data.database import get_session
from jobposts import jobpost_service as js
from utils import attribute_service as ats


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
        education = ats.view_education_by_id(new_job_ad, session)
        employment = ats.get_employment_by_id(new_job_ad, session)
        location = ats.get_location_by_id(new_job_ad, session)

        return JobAddResponse(
            title=new_job_ad.title,
            company_name=new_job_ad.company_name,
            company_description=new_job_ad.description,
            education=education,
            salary=new_job_ad.salary,
            employment=employment,
            location=location
        )
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
