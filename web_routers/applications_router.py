from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from common.template_config import CustomJinja2Templates
from data.database import get_session
from sqlmodel import Session
from utils import auth as au
from users.user_service import accepted_jobs, rejected_jobs, accepted_resumes, rejected_resumes
from companies.company_service import get_companies_by_owner_id
from matches.suggest_service import matched_jobs, matched_resumes

templates = CustomJinja2Templates(directory='templates')
router = APIRouter(prefix='/applications')

@router.get('/my_applications')
def show_my_applications(request: Request, session: Session = Depends(get_session)):

    token = request.cookies.get('token')
    user = au.get_current_user(token)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name='login.html',
            context={}
        )
    
    matched = matched_jobs(session=session, user_id=user.id)
    accepted_applications = [job for job in accepted_jobs(session=session, user_id=user.id) if job not in matched]
    rejected_applications = rejected_jobs(session=session, user_id=user.id)
    

    return templates.TemplateResponse(
        request=request,
        name='applications.html',
        context={'accepted_ads': jsonable_encoder([application.model_dump() for application in accepted_applications] if accepted_applications else None), 
                 'declined_ads': jsonable_encoder([application.model_dump() for application in rejected_applications] if rejected_applications else None),
                 'matched_ads': jsonable_encoder([application.model_dump() for application in matched] if matched else None)}
    )

@router.get('/company')
def show_companies_applications(request: Request, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name='login.html',
            context={}
        )
    
    matched = matched_resumes(session=session, user_id=user.id)
    accepted = [resume for resume in accepted_resumes(session=session, user_id=user.id) if resume not in matched]
    rejected = rejected_resumes(session=session, user_id=user.id)

    
    return templates.TemplateResponse(
        request=request,
        name='company-applications.html',
        context={'accepted_resumes': jsonable_encoder([resume.model_dump() for resume in accepted] if accepted_resumes else None),
                 'declined_resumes': jsonable_encoder([resume.model_dump() for resume in rejected] if rejected_resumes else None),
                'matched_resumes': jsonable_encoder([resume.model_dump() for resume in matched] if matched_resumes else None)}
    )