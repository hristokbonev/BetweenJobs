from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from common.template_config import CustomJinja2Templates
from data.database import get_session
from sqlmodel import Session
from utils import auth as au
from users.user_service import accepted_jobs, rejected_jobs
from companies.company_service import get_companies_by_owner_id

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
    
    accepted_applications = accepted_jobs(session=session, user_id=user.id)
    rejected_applications = rejected_jobs(session=session, user_id=user.id)

    return templates.TemplateResponse(
        request=request,
        name='applications.html',
        context={'accepted_ads': jsonable_encoder([application.model_dump() for application in accepted_applications] if accepted_applications else None), 
                 'declined_ads': jsonable_encoder([application.model_dump() for application in rejected_applications] if rejected_applications else None) }
    )

@router.get('/company')
def show_companies_applications(request: Request, session: Session = Depends(get_session)):
    token = request.cookies.get('token')
    user = au.get_current_user(token)
    companies = get_companies_by_owner_id(user.id, session)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name='login.html',
            context={}
        )
    
    return templates.TemplateResponse(
        request=request,
        name='companyapplications.html',
        context={'company': companies}
    )