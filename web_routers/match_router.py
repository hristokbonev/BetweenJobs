import os
from fastapi import APIRouter, Request, Depends, Form
from common.template_config import CustomJinja2Templates
from data.database import get_session
from sqlmodel import Session
from utils import auth as au
from matches import match_service as ms
from jobposts import jobpost_service as js
from resumes import resume_services as rs
from utils import attribute_service as ats
from datetime import timedelta


match_router = APIRouter(prefix='/match')
templates = CustomJinja2Templates(directory='templates')


# Navigate to Match page where resume should be selected to match job ad
@match_router.get('/{job_id}')
def match_preview(
    job_id: int,
    request: Request, 
    session: Session = Depends(get_session)
):
    # Get target job ad details
    target_job = js.view_job_post_by_id(job_id, session)
    deadline = target_job.created_at + timedelta(days=30)
    # Get required skills for the job post
    skills = ats.get_skills_for_job(target_job.id, session)
    # Get user resumes User is mandatory
    token = request.cookies.get('token')
    context={
        'request': request, 
        'jobad': target_job,
        'deadline': deadline,
        'skills': skills
    }

    if token:
        user = au.get_current_user(token)
        print(user)
        context['user'] = user
    else:
        return templates.TemplateResponse(
            request=request,
            name='login.html', 
            context=context
        ) 
    
    resume_list = rs.get_resumes_by_user_id(user.id, session)
    print(resume_list)
    context['resumes'] = resume_list

    return templates.TemplateResponse(
        request=request,
        name='match-single.html', 
        context=context
    )


@match_router.post('/{job_id}/match/{resume_id}')
def match_job_w_resume(
    job_id: int,
    resume_id: int,
    request: Request, 
    session: Session = Depends(get_session)
):
    # Retrieve job_id and user_id from cookies
    match_data = ms.match_with_job_ad(resume_id, job_id, session)
    token = request.cookies.get('token')
    
    base_url = os.getenv('base_url')
    context={
        'request': request, 
        'match': match_data,
        'baseurl': base_url
    }

    if token:
        user = au.get_current_user(token)
        context['user'] = user

    return templates.TemplateResponse(
        request=request,
        name='match.html', 
        context=context
    )