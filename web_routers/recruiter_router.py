from fastapi import APIRouter, Request, Depends, Query, Form, Response
from matches.suggest_service import insert_match_job_to_resume, insert_match_resume_to_job
from fastapi.encoders import jsonable_encoder
from data.database import get_session
from sqlmodel import Session
from utils import auth as au
from resumes import resume_services as rs
from matches import suggest_service as ss
from common.template_config import CustomJinja2Templates
from matches.match_models import JobFeedback, ResumeFeedback
from jobposts.jobpost_service import view_job_post_by_id

templates = CustomJinja2Templates(directory='templates')
router = APIRouter(prefix='/recruiter')

@router.get('/resume/{id}')
def recruit_resume(request: Request, id: int, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    resume = rs.get_resume_by_id(id=id, session=session)
    matches = ss.suggest_job_ads(resume_id=id, session=session)
    if resume.user_id != user.id:
        return Response(status_code=403)
    context = {
        'resume': jsonable_encoder(resume.model_dump()) if resume else None,
        'matches': jsonable_encoder([match.model_dump() for match in matches] if matches else None)
    }
    return templates.TemplateResponse(
        request=request,
        name='recruiter.html',
        context=context
    )

@router.get('/job/{id}')
def recruit_job(request: Request, id: int, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    job = view_job_post_by_id(ad_id=id, session=session)
    matches = ss.suggest_resumes(ad_id=id, session=session)
    context = {
        'job': jsonable_encoder(job.model_dump()) if job else None,
        'matches': jsonable_encoder([match.model_dump() for match in matches] if matches else None)
    }
    return templates.TemplateResponse(
        request=request,
        name='recruiter-job.html',
        context=context
    )

@router.post('/feedback')
def recruiter_feedback(request: Request, feedback: JobFeedback, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    if not user:
        return Response(status_code=403)
    
    insert_match_resume_to_job(resume_id=feedback.resume_id, job_ad_id=feedback.job_id, accepted=feedback.accepted, session=session)


@router.post('/feedback/job')
def recruiter_feedback_job(request: Request, feedback: ResumeFeedback, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    if not user:
        return Response(status_code=403)
    
    insert_match_job_to_resume(job_ad_id=feedback.job_id, session=session, accepted=True, resume_id=feedback.resume_id)
    