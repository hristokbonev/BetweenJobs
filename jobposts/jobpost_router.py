from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from common.exceptions import NotFoundException
from companies.company_models import JobAddResponse
from jobposts.jobpost_models import CreateJobAdRequest, UpdateJobAdRequest
from typing import Optional, Literal, List, Dict
from data.database import get_session
from jobposts import jobpost_service as js
from utils import attribute_service as ats


job_post_router = APIRouter(prefix='/api/jobad', tags=["JobAds"])


@job_post_router.get('/')
def show_all_job_ads(
        session: Session = Depends(get_session),
        page: int = 1,
        limit: int = 10,
        title: Optional[str] = None,
        company_name: Optional[str] = None,
        location: Optional[str] = Query(None),
        employment_type: Optional[Literal['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship', 'Volunteer']] = Query(None),
        education: Optional[Literal['High School', 'Undergraduate degree', 'Postgraduate degree', 'PhD', 'Diploma']] = Query(None),
        status: Optional[Literal['Active', 'Hidden', 'Private', 'Matched', 'Archived', 'Busy']] = Query(None),
        skills: Optional[List[str]] = Query(None)
):
    try:
        job_ads = js.show_all_posts(
            session=session,
            page=page,
            limit=limit,
            title=title,
            company_name=company_name,
            location=location,
            employment_type=employment_type,
            education=education,
            status=status
        )
        if not job_ads:
            raise NotFoundException(detail='No Job Ads found')
        return job_ads
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@job_post_router.get('/{job_id}', response_model=JobAddResponse)
def show_job_ad_by_id(job_id: int, session: Session = Depends(get_session)):
    try:
        job_ad = js.view_job_post_by_id(ad_id=job_id, session=session)
        if not job_ad:
            raise HTTPException(status_code=404, detail=f"Job Ad with ID {job_id} not found.")

        return job_ad
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
        js.change_job_post(job_id, data, session)
        updated_job = show_job_ad_by_id(job_id, session)
        return JobAddResponse(**dict(updated_job))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Server error: {str(e)}')


@job_post_router.delete('/{job_id}', response_model=Dict[str, str])
def delete_jobad_by_id(job_id: int, session: Session = Depends(get_session)):
    return js.delete_job_ad(job_id, session)