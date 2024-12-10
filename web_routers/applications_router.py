from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from common.template_config import CustomJinja2Templates
from data.database import get_session
from sqlmodel import Session
from utils import auth as au
from users.user_service import accepted_jobs, rejected_jobs

templates = CustomJinja2Templates(directory='templates')
router = APIRouter(prefix='/applications')

@router.get('/')
def show_applications(request: Request, session: Session = Depends(get_session)):

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
        context={'accepted': jsonable_encoder([application.model_dump() for application in accepted_applications] if accepted_applications else None), 
                 'declined': jsonable_encoder([application.model_dump() for application in rejected_applications] if rejected_applications else None) }
    )